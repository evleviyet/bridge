"""
Middleware to bridge Bolt.New and GitHub APIs.
"""
from typing import Dict, Any
from .bolt_new_client import BoltNewClient
from .github_client import GitHubClient

class APIBridgeMiddleware:
    def __init__(self):
        self.bolt_client = BoltNewClient()
        self.github_client = GitHubClient()

    def process_project_data(self, project_id: str) -> Dict[str, Any]:
        """Process project data from Bolt.New and prepare for GitHub."""
        project_data = self.bolt_client.fetch_project_data(project_id)
        return self._transform_project_data(project_data)

    def _transform_project_data(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Bolt.New project data to GitHub format."""
        return {
            'title': project_data.get('name', ''),
            'description': project_data.get('description', ''),
            'content': project_data.get('content', {})
        }