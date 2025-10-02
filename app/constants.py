import os

from dotenv import load_dotenv

load_dotenv()

# Supervisor model used as main agent overseeing sub-agents
SUPERVISOR_MODEL_API_KEY = os.getenv("SUPERVISOR_MODEL_API_KEY", "")
SUPERVISOR_MODEL_BASE_URL = os.getenv("SUPERVISOR_MODEL_BASE_URL", "")
SUPERVISOR_MODEL_NAME = os.getenv("SUPERVISOR_MODEL_NAME", "")
SUPERVISOR_MODEL_PROVIDER = os.getenv("SUPERVISOR_MODEL_PROVIDER", "")

# Researcher model used for conducting research
RESEARCHER_MODEL_API_KEY = os.getenv("RESEARCHER_MODEL_API_KEY", "")
RESEARCHER_MODEL_BASE_URL = os.getenv("RESEARCHER_MODEL_BASE_URL", "")
RESEARCHER_MODEL_NAME = os.getenv("RESEARCHER_MODEL_NAME", "")
RESEARCHER_MODEL_PROVIDER = os.getenv("RESEARCHER_MODEL_PROVIDER", "")

# Limits on resource usage
MAX_CONCURRENT_RESEARCH_UNITS = os.getenv("MAX_CONCURRENT_RESEARCH_UNITS", 3)
MAX_RESEARCHER_ITERATIONS = os.getenv("MAX_RESEARCHER_ITERATIONS", 3)

# Server settings
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))
SERVER_NAME = os.getenv("SERVER_NAME", "deep-learning-research-agent")
SERVER_LOG_LEVEL = os.getenv("SERVER_LOG_LEVEL", "info")
SERVER_RELOAD = os.getenv("SERVER_RELOAD", "true").lower() == "true"