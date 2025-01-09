"""
Data ingestion module for handling CSV and JSON files.
"""
import json
import csv
from typing import Dict, List, Any

class DataIngestion:
    @staticmethod
    def read_json(file_path: str) -> Dict[str, Any]:
        """Read JSON file and return dictionary."""
        with open(file_path, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def read_csv(file_path: str) -> List[Dict[str, str]]:
        """Read CSV file and return list of dictionaries."""
        data = []
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    @staticmethod
    def save_json(data: Dict[str, Any], file_path: str) -> None:
        """Save dictionary to JSON file."""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)