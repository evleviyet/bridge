"""
GitHub API istemcisi
"""
import os
import aiohttp
from typing import Dict, Any, Optional

class GitHubClient:
    def __init__(self):
        self.api_key = os.getenv("GITHUB_API_KEY")
        self.api_url = "https://api.github.com"
        
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """API isteği gönder"""
        headers = {
            "Authorization": f"token {self.api_key}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method,
                f"{self.api_url}{endpoint}",
                headers=headers,
                json=data
            ) as response:
                if response.status >= 400:
                    raise Exception(f"GitHub API Error: {await response.text()}")
                return await response.json()
                
    async def get_repository(self, owner: str, repo: str) -> Dict[str, Any]:
        """Depo bilgilerini al"""
        return await self._make_request("GET", f"/repos/{owner}/{repo}")
        
    async def create_pull_request(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str,
        branch: str,
        base: str = "main"
    ) -> Dict[str, Any]:
        """Pull request oluştur"""
        data = {
            "title": title,
            "body": body,
            "head": branch,
            "base": base
        }
        return await self._make_request(
            "POST",
            f"/repos/{owner}/{repo}/pulls",
            data
        )