"""
Helper functions for the integration bridge.
"""
import os
import json
from typing import Dict, Any

def load_env_vars() -> Dict[str, str]:
    """Load environment variables from .env file."""
    env_vars = {}
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
    return env_vars

def validate_response(response: Dict[str, Any]) -> bool:
    """Validate API response."""
    return isinstance(response, dict) and response.get('error') is None