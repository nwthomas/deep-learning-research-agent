"""
Deep Learning Research Agent FastAPI Server

Run with: python main.py
Server will be available at http://localhost:8000
WebSocket endpoint: ws://localhost:8000/ws/research
"""

import uvicorn
from src import SERVER_HOST, SERVER_PORT, SERVER_LOG_LEVEL, SERVER_RELOAD

if __name__ == "__main__":
    uvicorn.run(
        "src.api.server:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        log_level=SERVER_LOG_LEVEL,
        reload=SERVER_RELOAD
    )
