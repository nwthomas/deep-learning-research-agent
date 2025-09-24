from dotenv import load_dotenv
from src import run_agent

load_dotenv()

def main():
    run_agent("Give me an overview of Model Context Protocol (MCP).")

if __name__ == "__main__":
    main()
