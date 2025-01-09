"""
Tests for data ingestion module.
"""
import unittest
import json
import tempfile
import os
from src.core.data_ingestion import DataIngestion

class TestDataIngestion(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        
    def test_read_json(self):
        test_data = {"test": "data"}
        file_path = os.path.join(self.temp_dir, "test.json")
        
        with open(file_path, 'w') as f:
            json.dump(test_data, f)
            
        result = DataIngestion.read_json(file_path)
        self.assertEqual(result, test_data)

if __name__ == '__main__':
    unittest.main()