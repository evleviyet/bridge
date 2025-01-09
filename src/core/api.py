"""
FastAPI tabanlı dosya sistemi API'si
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from typing import Dict, List
import os

from .filesystem import BoltFileSystem
from .local_bridge import LocalBridge

app = FastAPI()
fs = BoltFileSystem()
local_bridge = LocalBridge()

@app.get("/check_env")
async def check_env():
    """Çevre değişkenlerini kontrol et"""
    try:
        local_path = os.getenv('BOLT_LOCAL_PATH')
        if not local_path:
            return {"status": "error", "message": "BOLT_LOCAL_PATH bulunamadı"}
            
        if not os.path.exists(local_path):
            return {"status": "error", "message": f"Belirtilen yol bulunamadı: {local_path}"}
            
        return {
            "status": "success",
            "local_path": local_path,
            "exists": True,
            "is_directory": os.path.isdir(local_path)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sync_local")
async def sync_local():
    """Yerel projeyi senkronize et"""
    try:
        result = await local_bridge.sync_local_project()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ... (diğer endpoint'ler) ...