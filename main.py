"""
Deep Learning Research Agent FastAPI Server

Run with: python main.py
Server will be available at http://localhost:8000
WebSocket endpoint: ws://localhost:8000/ws/research
"""

import uvicorn
from src import app

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False
    )
