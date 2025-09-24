> NOTE: This repository is in draft state as I'm building. However, I like learning in public so here it is.

# Deep Learning Research Agent

A multipurpose deep learning research agent 🔗

## Setup

1. **Install dependencies:**
   ```bash
   make install
   ```

2. **Set up API keys:**
   Create a `.env` file in the project root with the following variables:
   ```bash
   # Anthropic API Key - Required for content summarization
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   
   # Tavily API Key - Required for web search functionality  
   TAVILY_API_KEY=your_tavily_api_key_here
   
   # Optional: Local Ollama Configuration
   OLLAMA_BASE_URL=your_local_model_hostname_here
   OLLAMA_MODEL=your_model_name_here
   MODEL_PROVIDER=anthropic  # Set to 'local' to use Ollama by default
   ```

3. **Run the agent:**
   ```bash
   make run
   ```

## Usage

### Default Mode (Anthropic Claude)
```bash
python main.py --query "Your research question here"
```

### Local Mode (Ollama)
```bash
# Using command line flag
python main.py --local --query "Your research question here"

# Using environment variable (set MODEL_PROVIDER=local in .env)
python main.py --query "Your research question here"
```

## API Keys Required

- **Anthropic API Key**: Get one from [Anthropic Console](https://console.anthropic.com/) for content summarization
- **Tavily API Key**: Get one from [Tavily](https://tavily.com/) for web search functionality
