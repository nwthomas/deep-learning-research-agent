import argparse
import os
from dotenv import load_dotenv
from src import run_agent

load_dotenv()

def main():    
    run_agent("Please tell me about Claude Sonnet 4.5. Bias towards finding quick information and returning it in a concise manner.")

if __name__ == "__main__":
    main()
