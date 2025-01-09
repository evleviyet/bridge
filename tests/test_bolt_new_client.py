"""
Tests for Bolt.New API client.
"""
import unittest
from unittest.mock import patch
from src.core.bolt_new_client import BoltNewClient

class TestBoltNewClient(unittest.TestCase):
    def setUp(self):
        self.client = BoltNewClient()

    @patch('urllib.request.urlopen')
    def test_fetch_project_data(self, mock_urlopen):
        # Mock response data
        mock_response = {
            'id': '123',
            'name': 'Test Project',
            'description': 'Test Description'
        }
        
        # Configure mock
        mock_urlopen.return_value.__enter__.return_value.read.return_value = \
            json.dumps(mock_response).encode()

        # Test the method
        result = self.client.fetch_project_data('123')
        self.assertEqual(result, mock_response)

if __name__ == '__main__':
    unittest.main()