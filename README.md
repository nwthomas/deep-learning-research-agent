# Deep Learning Research Agent

A multipurpose deep learning research agent 🔗

This repository started as a combination of learning process and prototyping. It will remain public as proof of work and for others to use in their own journey if they want.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Setup](#setup)
    - [Repository](#repository)
    - [Environment Variables](#environment-variables)
    - [IDE](#ide)
    - [Coding](#coding)
3. [Issues, Bugs, and Project Management](#issues-bugs-and-project-management)
4. [Acknowledgements](#️-acknowledgements)

## Project Structure

```bash
├── .github/                 # Contains CODEOWNERS and GitHub action workflows
├── app/                     # Main application files
│   ├── agents/              # Agent creation, tool use, and prompts
│   ├── api/                 # Main applications files for server
│   └── shared/               # Shared code modules used throughout server
├── helm/                    # Helm charts
│   ├── templates/           #
│   ├── Chart.yaml           #
│   └── values.yaml          #
├── migrations/              # Terraform configurations
├── tests/                   # All testing files for server application
└── main.py                  # Root file for running server application
```

## Setup

### Repository

The following setup is needed for running this codebase correctly:

1. [Python](https://www.python.org) (through [Pyenv](https://github.com/pyenv/pyenv))
2. [Docker](https://www.docker.com)

First, ensure the proper Python version is installed locally. See the [.python-version](./.python-version) file for the recommended versioning.

Install `pyenv` first to manage non-system level Python installations. This can be done with:

```bash
# Install on MacOS
brew install pyenv

# Install on Linux
curl https://pyenv.run | bash

# Install on Windows
winget install pyenv.pyenv-win
```

Next, use `pyenv` to install Python:

```bash
# Install on MacOS, Linux, and Windows
pyenv install 3.12.4
pyenv global 3.12.4

# Check install afterwards
python --version
```

Next, install `uv` for package management and virtual environment setup for running the server:

```bash
# On MacOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After setting up Python and uv, run the following commands to fully configure local dev dependencies and git hooks for this codebase:

```base
make sync-dev
make install-hooks
```

Finally, Docker will need to be installed to run this codebase locally. The easiest way to do this is to just install and setup Docker Desktop. To do that, use one of the following links:

1. [Docker Desktop MacOS](https://docs.docker.com/desktop/setup/install/mac-install)
2. [Docker Desktop Linux](https://docs.docker.com/desktop/setup/install/linux)
3. [Docker Desktop Windows](https://docs.docker.com/desktop/setup/install/windows-install)

### Environment Variables

Create a new `.env` file in the root of the repository and set the required environment variables (using the [.env.example](https://github.com/nwthomas/deep-learning-research-agent/blob/main/.env.example) file as reference).

This repository supports both cloud-based models as well as those run locally (such as with [Ollama](https://ollama.com) or [vLLM](https://docs.vllm.ai)).

Note that setting an Anthropic/OpenAI key and model name does not require a base URL or provider name as those are automatically set by the underlying dependencies. However, locally run models will require all these environment variables to be filled out.

Here are two examples of configurations for cloud-based models and local, respectively. Each agent in the environment variable list can be customized individually:

```bash
# Leave the SUPERVISOR_MODEL_BASE_URL and SUPERVISOR_MODEL_PROVIDER blank for Anthropic usage as those are set
# automatically by LangChain.
SUPERVISOR_MODEL_API_KEY=api_key_here
SUPERVISOR_MODEL_BASE_URL=
SUPERVISOR_MODEL_NAME=claude-sonnet-4-5-20250929
SUPERVISOR_MODEL_PROVIDER=

# Setup for a locally-run LLM. The SUPERVISOR_MODEL_API_KEY likely won't matter here (unless it's set on the
# process serving the model) and is just required by LangChain's package. For a list of all possible providers that
# LangChain allows, see: https://python.langchain.com/api_reference/langchain/chat_models/langchain.chat_models.base.init_chat_model.html
SUPERVISOR_MODEL_API_KEY=ollama
SUPERVISOR_MODEL_BASE_URL=http://localhost:11434
SUPERVISOR_MODEL_NAME=gpt-oss:20b
SUPERVISOR_MODEL_PROVIDER=ollama
```

At time of this writing, [gpt-oss:20b](https://huggingface.co/openai/gpt-oss-20b) is an open source model that performs well with tool calls, thinking, and overall tasks for this repository's agent.

After all the above environment variable configurations, running `make dev` will automatically use the local `.env` file and start up the server in Docker.

### IDE

Formatting for the codebase can run on save. It's recommended to add the following IDE `settings.json` setup (in Cursor or VS Code, although it may be possible to figure out an analogous setup in another IDE):

```json
"[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.formatOnType": true,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

### Coding

Claude Code is the recommended choice for AI-assisted coding within this repository. There's already a `CLAUDE.md` file to govern how the model interacts with this codebase.

For more on Claude Code, see the [Anthropic Documentation](https://www.claude.com/product/claude-code).

## Issues, Bugs, and Project Management

🎯 To see upcoming work for this repository, see this [Trello board](https://trello.com/b/Qm5Ltjec/deep-learning-agent).

💬 If you want a feature, found a bug, or just want to contribute, read the [Contributing Guidelines](https://github.com/nwthomas/deep-learning-research-agent?tab=contributing-ov-file#contributing) and then open a new [GitHub issue](https://github.com/nwthomas/deep-learning-research-agent/issues/new).

🔓 Found a security vulnerability? Responsible and private disclosures are greatly appreciated. See [Security](https://github.com/nwthomas/deep-learning-research-agent?tab=security-ov-file) for next steps.

## Acknowledgements

- The [LangChain](https://www.langchain.com) team for their exceptional documentation and [LangChain Academy courses](https://academy.langchain.com).
