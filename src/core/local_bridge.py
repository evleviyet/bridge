"""
Local Bolt.New project bridge
"""
from ..config.local_config import LocalConfig
from .filesystem import BoltFileSystem

class LocalBridge:
    def __init__(self):
        self.config = LocalConfig()
        self.fs = BoltFileSystem()
        
    async def sync_local_project(self):
        """Yerel projeyi Bolt.New dosya sistemine senkronize et"""
        if not self.config.validate_path():
            raise ValueError("Geçersiz yerel proje yolu")
            
        # Projeyi oluştur
        self.fs.create_project(self.config.project_name)
        
        # Dosyaları kopyala
        for file_path in self.config.get_project_files():
            with open(os.path.join(self.config.local_project_path, file_path), 'r') as f:
                content = f.read()
                self.fs.write_file(
                    self.config.project_name,
                    file_path,
                    content,
                    "local_sync"
                )
        
        return {
            "status": "success",
            "project_name": self.config.project_name,
            "files_synced": len(self.config.get_project_files())
        }