import unittest
import json
from docusearch.app import app

class DocusearchTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_query_endpoint_success(self):
        payload = {
            "query": "Who is Travis Kalanick",
            "api_key": "sk-proj-0Jvj5nPhxGXNq0YhGXgiT3BlbkFJaa5m0E5xGfC6JO9YqG3u",
            "folder_path": "C:/Users/asay/OneDrive - Genmab/Desktop/Upload_Documents"
        }
        response = self.app.post('/query', json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("document_source", data)
        self.assertIn("answer", data)

    def test_query_endpoint_missing_query(self):
        payload = {
            "api_key": "sk-proj-0Jvj5nPhxGXNq0YhGXgiT3BlbkFJaa5m0E5xGfC6JO9YqG3u",
            "folder_path": "C:/Users/asay/OneDrive - Genmab/Desktop/Upload_Documents"
        }
        response = self.app.post('/query', json=payload)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Query text, API key, and folder path are required")

    def test_query_endpoint_invalid_folder_path(self):
        payload = {
            "query": "Who is Travis Kalanick",
            "api_key": "sk-proj-0Jvj5nPhxGXNq0YhGXgiT3BlbkFJaa5m0E5xGfC6JO9YqG3u",
            "folder_path": "/invalid/path"
        }
        response = self.app.post('/query', json=payload)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "The folder path does not exist")

if __name__ == '__main__':
    unittest.main()
