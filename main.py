import argparse
from src import run_agent

def main():
    parser = argparse.ArgumentParser(description="Deep Learning Research Agent")
    parser.add_argument("--query", type=str, required=True, help="Research query to process")
    parser.add_argument("--local", action="store_true", help="Use local models")

    args = parser.parse_args()
    run_agent(args.query)

if __name__ == "__main__":
    main()
