"""Deep Learning Research Agent FastAPI Server"""

import asyncio

import uvicorn

from app import SERVER_HOST, SERVER_LOG_LEVEL, SERVER_PORT, SERVER_RELOAD


async def main():
    uvicorn.run(
        "app.api.server:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        log_level=SERVER_LOG_LEVEL,
        reload=SERVER_RELOAD
    )

if __name__ == "__main__":
    asyncio.run(main())
