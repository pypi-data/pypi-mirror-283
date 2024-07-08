import openai
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import faiss
import pdfplumber
import numpy as np
from docx import Document
import logging
import time
import tiktoken  # For calculating token length
import platform
import zipfile
from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub
from odf.opendocument import load
from odf.text import P
import json 

# Setup logging
logging.basicConfig(level=logging.INFO)

# In-memory cache for storing processed documents, metadata, and embeddings
cache = {}

# Tokenizer to calculate token lengths
tokenizer = tiktoken.get_encoding('cl100k_base')

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ''
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ''
    except pdfplumber.pdfparser.PDFSyntaxError:
        logging.error(f"Error processing PDF file: {pdf_path}. The file is not a valid PDF.")
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return '\n'.join([para.text for para in doc.paragraphs])

# Function to extract text from TXT
def extract_text_from_txt(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to extract text from ODT
def extract_text_from_odt(odt_path):
    text = ''
    doc = load(odt_path)
    paragraphs = doc.getElementsByType(P)
    for paragraph in paragraphs:
        for node in paragraph.childNodes:
            if node.nodeType == 3:  # Node.TEXT_NODE
                text += node.data
            elif node.nodeType == 1:  # Node.ELEMENT_NODE
                text += node.firstChild.data if node.firstChild else ''
        text += '\n'
    return text

# Function to extract text from HTML files within a ZIP archive
def extract_text_from_html_zip(zip_path):
    text = ''
    with zipfile.ZipFile(zip_path, 'r') as z:
        for filename in z.namelist():
            if filename.endswith('.html'):
                with z.open(filename) as f:
                    soup = BeautifulSoup(f, 'html.parser')
                    text += soup.get_text() + '\n'
    return text

# Function to extract text from EPUB
def extract_text_from_epub(epub_path):
    text = ''
    book = epub.read_epub(epub_path)
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_body_content(), 'html.parser')
            text += soup.get_text() + '\n'
    return text

# Function to split text into chunks within token limits
def split_text_into_chunks(text, max_tokens):
    tokens = tokenizer.encode(text)
    chunks = []
    while tokens:
        chunk_tokens = tokens[:max_tokens]
        chunk_text = tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text)
        tokens = tokens[max_tokens:]
    return chunks

# Function to generate embeddings using OpenAI
def generate_embeddings(text, api_key):
    openai.api_key = api_key
    try:
        chunks = split_text_into_chunks(text, max_tokens=2048)  # Use a smaller chunk size for embeddings
        embeddings = []
        for chunk in chunks:
            response = openai.Embedding.create(
                input=chunk,
                model="text-embedding-ada-002"  # Use the appropriate model name
            )
            embeddings.append(response['data'][0]['embedding'])
    except openai.error.AuthenticationError:
        return None
    # Average the embeddings if multiple chunks
    return np.mean(embeddings, axis=0)

# Function to read documents from a directory and generate embeddings
def read_documents(directory, api_key):
    if directory in cache:
        logging.info(f"Loading documents from cache for directory: {directory}")
        return cache[directory]["documents"], cache[directory]["metadatas"], cache[directory]["ids"], cache[directory]["embeddings"], []

    logging.info(f"Processing documents in directory: {directory}")
    documents = []
    metadatas = []
    ids = []
    embeddings = []
    unsupported_files = []

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif filename.lower().endswith(".docx"):
            text = extract_text_from_docx(file_path)
        elif filename.lower().endswith(".txt"):
            text = extract_text_from_txt(file_path)
        elif filename.lower().endswith(".odt"):
            text = extract_text_from_odt(file_path)
        elif filename.lower().endswith(".zip"):
            text = extract_text_from_html_zip(file_path)
        elif filename.lower().endswith(".epub"):
            text = extract_text_from_epub(file_path)
        else:
            unsupported_files.append(filename)
            continue
        
        if not text:
            logging.warning(f"Skipped empty or invalid file: {file_path}")
            continue
        
        documents.append(text)
        metadata = {"source": filename}
        metadatas.append(metadata)
        doc_id = os.path.splitext(filename)[0]
        ids.append(doc_id)
        
        # Generate and store embeddings
        document_embedding = generate_embeddings(text, api_key)
        if document_embedding is None:
            return None, None, None, None, unsupported_files
        embeddings.append(document_embedding)
    
    # Convert embeddings to a 2D numpy array
    embeddings = np.array(embeddings)
    
    # Store processed documents in cache
    cache[directory] = {
        "documents": documents,
        "metadatas": metadatas,
        "ids": ids,
        "embeddings": embeddings
    }
    
    return documents, metadatas, ids, embeddings, unsupported_files

# Function to split the document into chunks dynamically for querying
def split_document(document, max_tokens=4096):  # Adjust the max_tokens value for queries
    return split_text_into_chunks(document, max_tokens=max_tokens)

# Function to query the OpenAI API for a document chunk
def query_chunk(chunk_num, chunk, question, api_key):
    openai.api_key = api_key
    max_completion_tokens = 512  # Limit the number of tokens for the completion
    max_input_tokens = 8192 - max_completion_tokens  # Ensure the total tokens do not exceed the limit
    chunk = split_text_into_chunks(chunk, max_input_tokens)[0]  # Ensure chunk is within input token limit
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Document chunk {chunk_num}:\n{chunk}\n\nQuestion: {question}\n\nProvide an answer and cite sentences from the document."}
        ],
        max_tokens=max_completion_tokens  # Ensure the response is within the model's maximum context length
    )
    return chunk_num, response.choices[0].message['content']

# Function to get the answer and citations using parallel processing
def get_answers_with_citations(question, document_chunks, api_key):
    all_evidence = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(query_chunk, i+1, chunk, question, api_key) for i, chunk in enumerate(document_chunks)]
        for future in as_completed(futures):
            chunk_num, answer = future.result()
            all_evidence.append((chunk_num, answer))
    return all_evidence

# Function to combine answers and citations
def combine_answers_with_citations(evidence_list):
    combined_answer = ""
    citations = []
    for chunk_num, answer in evidence_list:
        combined_answer += f"\n{answer}"
        sentences = [sent.strip() for sent in answer.split('.') if any(word in sent for word in answer.split())]
        citations.extend(sentences)
    return combined_answer, citations

# Function to query FAISS index
def query_index(query_embedding, index, metadatas, documents, embeddings, n_results=1):
    query_embedding = np.array([query_embedding]).astype('float32')  # Ensure it's a 2D array
    distances, indices = index.search(query_embedding, n_results)
    results = []
    for i in range(n_results):
        result = {
            'distance': distances[0][i],
            'metadata': metadatas[indices[0][i]],
            'document': documents[indices[0][i]],
            'embedding': embeddings[indices[0][i]]
        }
        results.append(result)
    return results

# Function to process the best matching document for a given query
def process_best_matching_document(query_text, api_key, folder_path):
    # Detect and normalize folder path based on the operating system
    folder_path = normalize_folder_path(folder_path)

    # Read documents and generate embeddings
    start_time = time.time()
    documents, metadatas, ids, embeddings, unsupported_files = read_documents(folder_path, api_key)
    if documents is None:
        return None, None, unsupported_files
    processing_time = time.time() - start_time
    logging.info(f"Document processing time: {processing_time:.2f} seconds")
    
    embedding_dim = embeddings.shape[1]  # Use shape attribute to get dimension
    embedding_matrix = np.array(embeddings).astype('float32')
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(embedding_matrix)
    
    # Generate query embedding
    query_embedding = generate_embeddings(query_text, api_key)
    if query_embedding is None:
        return None, None, unsupported_files
    
    # Query the FAISS index
    start_time = time.time()
    results = query_index(query_embedding, index, metadatas, documents, embeddings)
    querying_time = time.time() - start_time
    logging.info(f"Querying time: {querying_time:.2f} seconds")
    
    # Get the best matching document details
    best_result = results[0]
    best_document = best_result['document']
    best_metadata = best_result['metadata']['source']
    
    # Split the best matching document into chunks
    document_chunks = split_document(best_document)
    
    # Get answers and citations using parallel processing
    evidence_list = get_answers_with_citations(query_text, document_chunks, api_key)
    
    # Combine answers and extract citations
    answer, citations = combine_answers_with_citations(evidence_list)
    
    return best_metadata, answer, unsupported_files

# Function to normalize folder paths based on the detected operating system
def normalize_folder_path(folder_path):
    user_os = platform.system().lower()
    
    if 'windows' in user_os:
        if folder_path.startswith('/mnt/c'):
            folder_path = folder_path.replace('/mnt/c', 'C:').replace('/', '\\')
        else:
            folder_path = folder_path.replace('C:', '/mnt/c').replace('\\', '/')
    elif 'darwin' in user_os or 'linux' in user_os:
        if folder_path[1] == ':':
            folder_path = folder_path.replace('C:', '/mnt/c').replace('\\', '/')
        else:
            folder_path = folder_path.replace('\\', '/')
    
    return folder_path

# Main function to process a query
def process_query(query_text, api_key, folder_path):
    if not query_text or not api_key or not folder_path:
        raise ValueError("Query text, API key, and folder path are required")
    
    # Normalize folder path
    folder_path = normalize_folder_path(folder_path)
    
    if not os.path.exists(folder_path):
        logging.error(f"The folder path does not exist: {folder_path}")
        raise FileNotFoundError(f"The folder path does not exist: {folder_path}")
    
    best_metadata, answer, unsupported_files = process_best_matching_document(query_text, api_key, folder_path)
    
    if best_metadata is None:
        raise ValueError("Invalid API key")
    
    response = {
        "document_source": best_metadata,
        "answer": answer
    }
    
    if unsupported_files:
        response["warning"] = f"The following files are unsupported and were not processed: {', '.join(unsupported_files)}"
    
    return response

# If you want to use the script from the command line
if __name__ == '__main__':
    import argparse
    import json

    parser = argparse.ArgumentParser(description='Process a query with document search.')
    parser.add_argument('query', type=str, help='The query to search for')
    parser.add_argument('api_key', type=str, help='Your OpenAI API Key')
    parser.add_argument('folder_path', type=str, help='The path to your folder containing the files')

    args = parser.parse_args()
    result = process_query(args.query, args.api_key, args.folder_path)
    print(json.dumps(result, indent=2))

