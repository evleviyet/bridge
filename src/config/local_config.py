"""
Local Bolt.New project configuration
"""
import os
from pathlib import Path

class LocalConfig:
    def __init__(self):
        self.local_project_path = os.getenv('BOLT_LOCAL_PATH', '')
        self.project_name = os.path.basename(self.local_project_path)
        
    def validate_path(self) -> bool:
        """Yerel proje yolunun geçerliliğini kontrol et"""
        return os.path.exists(self.local_project_path)
        
    def get_project_files(self) -> list:
        """Proje dosyalarını listele"""
        files = []
        if self.validate_path():
            for root, _, filenames in os.walk(self.local_project_path):
                for filename in filenames:
                    full_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(full_path, self.local_project_path)
                    files.append(rel_path)
        return files