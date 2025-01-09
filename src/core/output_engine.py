"""
Output engine for generating reports.
"""
import json
from typing import Dict, Any

class OutputEngine:
    @staticmethod
    def generate_report(metrics: Dict[str, Any], output_file: str) -> None:
        """Generate and save a JSON report."""
        report = {
            "metrics": metrics,
            "timestamp": "1970-01-01 00:00:00"  # Using fixed timestamp for 1970
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)