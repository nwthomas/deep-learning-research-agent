import argparse
import asyncio
from src import run_agent

async def main():
    parser = argparse.ArgumentParser(description="Deep Learning Research Agent")
    parser.add_argument("--query", type=str, required=True, help="Research query to process")

    args = parser.parse_args()
    await run_agent(args.query)

if __name__ == "__main__":
    asyncio.run(main())
