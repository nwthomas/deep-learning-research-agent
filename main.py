import argparse
import os
from dotenv import load_dotenv
from src import run_agent

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Run the deep learning research agent")
    parser.add_argument(
        "--local", 
        action="store_true", 
        help="Use local Ollama model instead of Anthropic Claude"
    )
    parser.add_argument(
        "--query", 
        type=str, 
        default="Give me an overview of Model Context Protocol (MCP).",
        help="The query to run the agent with"
    )
    
    args = parser.parse_args()
    
    # Check if MODEL_PROVIDER environment variable is set
    model_provider = os.getenv("MODEL_PROVIDER", "anthropic")
    use_local = args.local or (model_provider == "local")
    
    print(f"Running agent with {'local Ollama model' if use_local else 'Anthropic Claude'}")
    if use_local:
        ollama_model = os.getenv("MODEL_NAME", "deepseek-r1:32b")
        print(f"Using Ollama model: {ollama_model}")
    
    run_agent(args.query, use_local=use_local)

if __name__ == "__main__":
    main()
