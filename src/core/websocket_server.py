"""
Basic WebSocket server implementation.
"""
import socket
from typing import Optional

class WebSocketServer:
    def __init__(self, host: str = 'localhost', port: int = 8765):
        self.host = host
        self.port = port
        self.socket: Optional[socket.socket] = None
        
    def start(self) -> None:
        """Start the WebSocket server."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        
    def stop(self) -> None:
        """Stop the WebSocket server."""
        if self.socket:
            self.socket.close()
            self.socket = None