"""
Bolt.New API istemcisi
"""
import os
import json
import aiohttp
from typing import Dict, Any, Optional

class BoltNewClient:
    def __init__(self):
        self.api_key = os.getenv("BOLT_NEW_API_KEY")
        self.api_url = os.getenv("BOLT_NEW_API_URL", "https://api.bolt.new")
        
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """API isteği gönder"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
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
                    raise Exception(f"API Error: {await response.text()}")
                return await response.json()
                
    async def fetch_instruction(self, instruction_id: str) -> Dict[str, Any]:
        """Talimat detaylarını al"""
        return await self._make_request("GET", f"/instructions/{instruction_id}")
        
    async def update_status(
        self, 
        instruction_id: str, 
        status: str,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None
    ) -> Dict[str, Any]:
        """Talimat durumunu güncelle"""
        data = {
            "status": status,
            "result": result,
            "error": error
        }
        return await self._make_request(
            "POST", 
            f"/instructions/{instruction_id}/status",
            data
        )
        
    async def sync_repository(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Depo bilgilerini Bolt.New ile senkronize et"""
        return await self._make_request(
            "POST",
            "/repositories/sync",
            repo_data
        )