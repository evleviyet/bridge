"""
Bolt.New için dosya sistemi yönetimi
"""
import os
import json
import shutil
from datetime import datetime
from typing import Dict, List, Optional

class BoltFileSystem:
    def __init__(self, base_path: str = "bolt_new_filesystem"):
        self.base_path = base_path
        self._ensure_base_directory()
        self.locks: Dict[str, str] = {}  # file_path: user_id
        
    def _ensure_base_directory(self) -> None:
        """Ana dizini oluştur"""
        os.makedirs(self.base_path, exist_ok=True)
        
    def create_project(self, project_name: str) -> bool:
        """Yeni proje dizini oluştur"""
        project_path = os.path.join(self.base_path, project_name)
        try:
            os.makedirs(project_path)
            return True
        except FileExistsError:
            return False
            
    def write_file(self, project_name: str, file_name: str, content: str, user_id: str) -> bool:
        """Dosya yaz ve versiyonla"""
        file_path = os.path.join(self.base_path, project_name, file_name)
        
        # Kilidi kontrol et
        if file_path in self.locks and self.locks[file_path] != user_id:
            return False
            
        # Mevcut dosyayı yedekle
        if os.path.exists(file_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{file_path}.v{timestamp}"
            shutil.copy2(file_path, backup_path)
            
        # Yeni içeriği yaz
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
        
    def read_file(self, project_name: str, file_name: str) -> Optional[str]:
        """Dosya oku"""
        file_path = os.path.join(self.base_path, project_name, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return None
            
    def lock_file(self, project_name: str, file_name: str, user_id: str) -> bool:
        """Dosyayı kilitle"""
        file_path = os.path.join(self.base_path, project_name, file_name)
        if file_path not in self.locks:
            self.locks[file_path] = user_id
            return True
        return False
        
    def unlock_file(self, project_name: str, file_name: str, user_id: str) -> bool:
        """Dosya kilidini kaldır"""
        file_path = os.path.join(self.base_path, project_name, file_name)
        if file_path in self.locks and self.locks[file_path] == user_id:
            del self.locks[file_path]
            return True
        return False
        
    def search_files(self, query: str) -> List[Dict[str, str]]:
        """Dosyalarda arama yap"""
        results = []
        for root, _, files in os.walk(self.base_path):
            for file in files:
                if not file.endswith('.v'):  # Versiyon dosyalarını atla
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if query.lower() in content.lower() or query.lower() in file.lower():
                                rel_path = os.path.relpath(file_path, self.base_path)
                                results.append({
                                    "path": rel_path,
                                    "matches": content.lower().count(query.lower())
                                })
                    except UnicodeDecodeError:
                        continue  # Binary dosyaları atla
        return results