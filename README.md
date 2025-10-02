> NOTE: This repository is in draft state as I'm building. It may well be the foundation of my future startup, but I like learning in public so here it is.

# 🧠🤖 Deep Learning Research Agent

A multipurpose deep learning research agent 🔗

## 🧱 Project Managements

Work for this repository is housed in this [Trello board](https://trello.com/b/Qm5Ltjec/deep-learning-agent).

## Repository Setup

It's recommended to use Claude Code with this repository. There's a `CLAUDE.md` file to govern how the model interacts with this codebase.

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

Finally, setup formatting for the codebase (particularly on save). It's recommended to add the following to your IDE's `settings.json (in Cursor or VS Code, although you may be able to figure out an analogous setup in another IDE of your choice):

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

## 🙇🏻‍♂️ Acknowledgements

- The [LangChain](https://www.langchain.com) team for their exceptional documentation and [LangChain Academy courses](https://academy.langchain.com).