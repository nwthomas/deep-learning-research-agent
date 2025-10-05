> NOTE: This repository is in draft state as I'm building. It may well be the foundation of my future startup, but I like learning in public so here it is.

# Deep Learning Research Agent

A multipurpose deep learning research agent 🔗

## Table of Contents

1. [Setup](#setup)
    - [Coding](#coding)
    - [Repository](#repository)
    - [IDE](#ide)
    - [Environment Variables](#environment-variables)
2. [Issues, Bugs, and Project Management](#issues-bugs-and-project-management)
3. [Acknowledgements](#️-acknowledgements)

## Issues, Bugs, and Project Management

🎯 To see upcoming work for this repository, see this [Trello board](https://trello.com/b/Qm5Ltjec/deep-learning-agent).
💬 If you want a feature, found a bug, or just want to contribute, read the [Contributing Guidelines](https://github.com/nwthomas/deep-learning-research-agent?tab=contributing-ov-file#contributing) and then open a new [GitHub issue](https://github.com/nwthomas/deep-learning-research-agent/issues/new).
🔓 Found a security vulnerability? We greatly appreciate responsible and private disclosures. See [Security](https://github.com/nwthomas/deep-learning-research-agent?tab=security-ov-file) for next steps.

## Setup

### Coding

It's recommended to use Claude Code for coding within this repository. There's already a `CLAUDE.md` file to govern how the model interacts with this codebase.

For more on Claude Code, see the [Anthropic Documentation](https://www.claude.com/product/claude-code).

### Repository

You'll need the following setup for running this codebase correctly:

1. [Python](https://www.python.org) (through [Pyenv](https://github.com/pyenv/pyenv))
2. [Docker](https://www.docker.com)

First, ensure you have the proper Python version locally. See the [.python-version](./.python-version) file for the recommended versioning.

You'll want to install `pyenv` first to manage non-system level Python installations. You can do that with:

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
pyenv install 3.12.6
pyenv global 3.12.6

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

After setting up Python and uv, you can run the following commands to fully configure dependencies and git hooks for this codebase:

```base
make sync-dev
make install-hooks
```

Finally, you will need to install Docker in order to run this codebase locally. The easiest way to do this is to just install and setup Docker Desktop. To do that, use one of the following links:

1. [Docker Desktop MacOS](https://docs.docker.com/desktop/setup/install/mac-install)
2. [Docker Desktop Linux](https://docs.docker.com/desktop/setup/install/linux)
3. [Docker Desktop Windows](https://docs.docker.com/desktop/setup/install/windows-install)

### IDE

You can setup formatting for the codebase (particularly on save). It's recommended to add the following to your IDE's `settings.json (in Cursor or VS Code, although you may be able to figure out an analogous setup in another IDE of your choice):

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

### Environment Variables

Create a new `.env` file in the root of your local repository and set the required environment variables.

This repository supports both cloud-based models as well as ones you might choose to run locally (such as with [Ollama](https://ollama.com) or [vLLM](https://docs.vllm.ai)).

Here are two examples of configurations for cloud-based models and local, respectively. You'll need to change these for each agent in the environment variable list (and can actually customize them individually):

```bash
# Leave the SUPERVISOR_MODEL_BASE_URL and SUPERVISOR_MODEL_PROVIDER blank for Anthropic usage as those are set
# automatically by LangChain.
SUPERVISOR_MODEL_API_KEY=your_api_key_here
SUPERVISOR_MODEL_BASE_URL=
SUPERVISOR_MODEL_NAME=claude-sonnet-4-5-20250929
SUPERVISOR_MODEL_PROVIDER=

# Setup for a locally-run LLM. The SUPERVISOR_MODEL_API_KEY likely won't matter here (unless you have one set on the
# process serving your model) and is just required by LangChain's package. For a list of all possible providers that
# LangChain allows, see: https://python.langchain.com/api_reference/langchain/chat_models/langchain.chat_models.base.init_chat_model.html
SUPERVISOR_MODEL_API_KEY=ollama
SUPERVISOR_MODEL_BASE_URL=http://localhost:11434
SUPERVISOR_MODEL_NAME=llama3.1:8b
SUPERVISOR_MODEL_PROVIDER=ollama
```

Running `make dev` will automatically use your local `.env` file.

## Acknowledgements

- The [LangChain](https://www.langchain.com) team for their exceptional documentation and [LangChain Academy courses](https://academy.langchain.com).
