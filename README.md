> NOTE: This repository is in draft state as I'm building. However, I like learning in public so here it is.

# Deep Learning Research Agent

A multipurpose deep learning research agent 🔗

## Setup

### Option 1: Local Development

1. **Install dependencies:**
   ```bash
   make sync
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

### Option 2: Docker

1. **Set up environment:**
   ```bash
   # Copy the Docker environment template
   cp env.docker.template .env
   # Edit .env with your actual API keys
   ```

2. **Build and run with Docker:**
   ```bash
   # Build the Docker image
   make docker-build
   
   # Run the container
   make docker-run
   ```

3. **Or use Docker Compose (recommended):**
   ```bash
   # Start the service
   make docker-compose-up
   
   # View logs
   make docker-compose-logs
   
   # Stop the service
   make docker-compose-down
   ```

## Usage

### Local Development

#### Default Mode (Anthropic Claude)
```bash
python main.py --query "Your research question here"
```

#### Local Mode (Ollama)
```bash
# Using command line flag
python main.py --local --query "Your research question here"

# Using environment variable (set MODEL_PROVIDER=local in .env)
python main.py --query "Your research question here"
```

### Docker Usage

#### Run with custom query
```bash
# Using Docker directly
docker run --rm -it --env-file .env deep-learning-research-agent python main.py --query "Your research question here"

# Using Docker Compose
docker-compose run --rm research-agent python main.py --query "Your research question here"
```

#### Interactive Docker session
```bash
# Get a shell inside the container
make docker-run-interactive

# Or with docker-compose
docker-compose run --rm research-agent bash
```

## Kubernetes Deployment with Helm

### Prerequisites
- Kubernetes cluster
- Helm 3.x installed
- Docker image built and pushed to a registry

### Deploy with Helm

1. **Build and push Docker image:**
   ```bash
   make docker-build
   docker tag deep-learning-research-agent your-registry/deep-learning-research-agent:latest
   docker push your-registry/deep-learning-research-agent:latest
   ```

2. **Install with Helm:**
   ```bash
   # Basic installation
   make helm-install
   
   # Or with custom values
   helm install deep-learning-research-agent helm/deep-learning-research-agent \
     --set image.repository=your-registry/deep-learning-research-agent \
     --set secrets.anthropicApiKey=your-api-key \
     --set secrets.tavilyApiKey=your-api-key
   ```

3. **Deploy with custom values:**
   ```bash
   # Override specific values
   helm install deep-learning-research-agent helm/deep-learning-research-agent \
     --set image.repository=your-registry/deep-learning-research-agent \
     --set secrets.anthropicApiKey=your-api-key \
     --set secrets.tavilyApiKey=your-api-key \
     --set ingress.enabled=true \
     --set ingress.hosts[0].host=research-agent.your-domain.com
   ```

### ArgoCD Deployment

1. **Apply the ArgoCD application:**
   ```bash
   kubectl apply -f argocd-application.yaml
   ```

2. **Monitor deployment:**
   ```bash
   kubectl get applications -n argocd
   ```

### Available Helm Commands

```bash
# Lint the chart
make helm-lint

# Template the chart
make helm-template

# Dry run installation
make helm-dry-run

# Install/upgrade/uninstall
make helm-install
make helm-upgrade
make helm-uninstall

# Package the chart
make helm-package
```

## API Keys Required

- **Anthropic API Key**: Get one from [Anthropic Console](https://console.anthropic.com/) for content summarization
- **Tavily API Key**: Get one from [Tavily](https://tavily.com/) for web search functionality
