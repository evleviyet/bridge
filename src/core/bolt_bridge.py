"""
Bolt.New ve GitHub API'leri arasında köprü katmanı
"""
from typing import Dict, Any, Optional
from .bolt_new_client import BoltNewClient
from .github_client import GitHubClient

class BoltGitHubBridge:
    def __init__(self):
        self.bolt_client = BoltNewClient()
        self.github_client = GitHubClient()
        
    async def process_instruction(self, instruction_id: str) -> Dict[str, Any]:
        """Bolt.New'dan gelen talimatı işle ve GitHub'a uygula"""
        try:
            # Talimatı al
            instruction = await self.bolt_client.fetch_instruction(instruction_id)
            
            # GitHub işlemlerini gerçekleştir
            if instruction["type"] == "create_pr":
                result = await self.github_client.create_pull_request(
                    owner=instruction["repo_owner"],
                    repo=instruction["repo_name"],
                    title=instruction["pr_title"],
                    body=instruction["pr_description"],
                    branch=instruction["branch"]
                )
                
                # Durumu Bolt.New'a bildir
                await self.bolt_client.update_status(
                    instruction_id,
                    status="completed",
                    result=result
                )
                
                return {"status": "success", "pr_url": result["html_url"]}
                
        except Exception as e:
            await self.bolt_client.update_status(
                instruction_id,
                status="failed",
                error=str(e)
            )
            raise
            
    async def sync_repository(self, repo_owner: str, repo_name: str) -> Dict[str, Any]:
        """GitHub deposunu Bolt.New ile senkronize et"""
        try:
            # GitHub'dan repo bilgilerini al
            repo_data = await self.github_client.get_repository(repo_owner, repo_name)
            
            # Bolt.New'a repo bilgilerini gönder
            sync_result = await self.bolt_client.sync_repository(repo_data)
            
            return {
                "status": "success",
                "repository": repo_data["full_name"],
                "sync_id": sync_result["sync_id"]
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}