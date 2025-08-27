# Smart Librarian — Final Documentation

A Windows-friendly RAG assistant that indexes your local content and lets you chat with it using OpenAI models. This project ships with one-click automation, reproducible environments, and an optional EXE build.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Requirements](#requirements)
- [Project Structure](#project-structure)
- [Setup & Installation (Windows)](#setup--installation-windows)
- [Quickstart](#quickstart)
- [Environment Variables](#environment-variables)
- [Building the Index](#building-the-index)
- [Running the Chat App](#running-the-chat-app)
- [Smoke Test](#smoke-test)
- [Packaging to a Single EXE (PyInstaller)](#packaging-to-a-single-exe-pyinstaller)
- [Troubleshooting](#troubleshooting)
- [Security Notes](#security-notes)
- [Roadmap / Next Steps](#roadmap--next-steps)
- [License](#license)

## Overview

**Smart Librarian** is a Retrieval-Augmented Generation (RAG) application. It:

- Builds a vector index from your content
- Uses OpenAI models to answer questions about that content
- Can be bootstrapped on Windows with a single batch command
- Can be packaged as a portable `.exe`

The repository is designed to be zero-friction on Windows: `win_scripts/` contains orchestration scripts, and the root has a single `smart_librarian.bat` launcher.

## Key Features

- **One-click Windows bootstrap** (`smart_librarian.bat`) → create venv, set env, build index, run chat
- **Reproducible env** with Python virtual environment and pinned requirements
- **Configurable models** (chat + embeddings) via environment variables
- **Persistent vector store** (Chroma) in a local folder you control
- **Optional EXE** build with PyInstaller for easy distribution to non-Python users

## Requirements

- Windows 10/11
- Python 3.10+ available on PATH (via `py` launcher or `python`)
- OpenAI API key with access to your chosen models
- Internet connectivity (for API calls)

If you plan to pack an `.exe`, you also need **PyInstaller** (installed into the project venv only for building).

## Project Structure

This documentation assumes the **existing structure is preserved**; only Windows batch files live in `win_scripts/` and the one-click launcher is at the root.

```
project_root/
│
├─ smart_librarian/         # your application package (unchanged)
│   ├─ __init__.py
│   ├─ main.py              # app entrypoint (CLI)
│   ├─ rag.py               # retrieval / RAG logic
│   ├─ tooling.py           # helper utilities
│   └─ ...
│
├─ scripts/                 # Python utility scripts (unchanged)
│   └─ build_index.py       # builds or updates the vector index
│
├─ tests/
│   └─ smoke_retrieval.py   # quick retrieval sanity check
│
├─ win_scripts/             # Windows automation (moved here)
│   ├─ install.bat
│   ├─ setup_env.bat
│   ├─ build_index.bat      # calls: python scripts\build_index.py
│   ├─ smoke.bat            # calls: python tests\smoke_retrieval.py
│   └─ chat.bat             # calls: python -m smart_librarian.main (checks OPENAI_API_KEY)
│
├─ smart_librarian.bat      # one-click launcher (install → env → index → chat)
├─ requirements.txt
└─ pyproject.toml           # optional (entry points, metadata, deps)
```

## Setup & Installation (Windows)

1. **Clone and open a terminal in the project root**
    ```bat
    cd path\to\project_root
    ```

2. **One-time installation of dependencies**
    ```bat
    win_scripts\install.bat
    ```
    This creates `.venv` in the root (if not present), upgrades pip, and installs from requirements.txt.

3. **Provide your OpenAI API key**

    There are two convenient options:

    - **Ephemeral (current terminal session only)**
      ```bat
      set OPENAI_API_KEY=sk-...your-key...
      win_scripts\setup_env.bat %OPENAI_API_KEY%
      ```
    - **Persistent (Environment Variables)**
      Add `OPENAI_API_KEY` via System Properties → Environment Variables, or run:
      ```bat
      setx OPENAI_API_KEY "sk-...your-key..."
      ```
      Then:
      ```bat
      win_scripts\setup_env.bat %OPENAI_API_KEY%
      ```
    `setup_env.bat` also sets sensible defaults for `CHAT_MODEL`, `EMBEDDING_MODEL`, and `CHROMA_DIR` if you don’t pass them as arguments.

## Quickstart

**One-click launcher (recommended)**

From the project root:
```bat
smart_librarian.bat
```
This runs, in order:
```
win_scripts\install.bat
win_scripts\setup_env.bat %OPENAI_API_KEY%
win_scripts\build_index.bat
win_scripts\chat.bat
```
Each step short-circuits on error (the chain stops immediately if something fails).

Tip: If your key is not in the environment, you can edit `smart_librarian.bat` to hardcode it or keep passing `%OPENAI_API_KEY%`.

## Environment Variables

- `OPENAI_API_KEY` (required) — your OpenAI key
- `CHAT_MODEL` (optional; default: gpt-4o-mini) — chat/completions model
- `EMBEDDING_MODEL` (optional; default: text-embedding-3-small) — embedding model used for indexing
- `CHROMA_DIR` (optional; default: <repo>\chroma) — local directory where ChromaDB stores its data

`win_scripts\setup_env.bat` sets defaults if you don’t provide arguments. You can override later by re-running it or exporting variables in your terminal.

## Building the Index

To (re)build the vector index:
```bat
win_scripts\build_index.bat
```
This activates the venv, sets PYTHONPATH to the repo root, and runs:
```bat
python scripts\build_index.py
```
Adjust `scripts\build_index.py` to point at your data sources (e.g., `data/` or `smart_librarian/data/`). The script should read raw files, compute embeddings with `EMBEDDING_MODEL`, and persist them into `CHROMA_DIR`.

## Running the Chat App

Start the chat CLI:
```bat
win_scripts\chat.bat
```
`chat.bat` verifies that `OPENAI_API_KEY` is defined and aborts with a non-zero exit code if it’s missing. It then runs:
```bat
python -m smart_librarian.main
```
Your `smart_librarian/main.py` should load the index from `CHROMA_DIR`, execute retrieval, and generate answers via the OpenAI API with `CHAT_MODEL`.

## Smoke Test

A quick sanity check for retrieval quality:
```bat
win_scripts\smoke.bat
```
This executes the Python test directly:
```bat
python tests\smoke_retrieval.py
```
If you prefer running it as a module (`python -m tests.smoke_retrieval`), make sure `tests/__init__.py` exists.

## Packaging to a Single EXE (PyInstaller)

Activate the venv, then build:
```bat
call .venv\Scripts\activate.bat
pyinstaller --onefile --name SmartLibrarian ^
  --collect-all smart_librarian ^
  --add-data "smart_librarian\data;smart_librarian\data" ^
  -p . smart_librarian\main.py
```
This produces `dist\SmartLibrarian.exe`.

### Accessing Data Files in EXE

If your data lives inside the package (`smart_librarian/data`), `--collect-all` and `--add-data` will bundle it.

If you keep data outside the package (e.g., top-level `data/`), either:

- add `--add-data "data;data"` and handle paths accordingly, or
- implement a helper that checks packaged resources and the executable’s directory (e.g., via `importlib.resources` and `sys._MEIPASS`).

### Running the EXE

The EXE still requires `OPENAI_API_KEY`. You can create a small `SmartLibrarian.exe.bat` in the same folder:
```bat
@echo off
set "OPENAI_API_KEY=sk-..."
set "CHAT_MODEL=gpt-4o-mini"
set "EMBEDDING_MODEL=text-embedding-3-small"
set "CHROMA_DIR=%cd%\chroma"
start "" "%~dp0SmartLibrarian.exe"
```

## Troubleshooting

- **[!] OPENAI_API_KEY is not set**  
  Export the key in your terminal or set it in System Environment Variables, then rerun `win_scripts\setup_env.bat %OPENAI_API_KEY%`.

- **No module named smart_librarian.main**  
  Ensure `smart_librarian/__init__.py` exists and that you run from the project root (the scripts do `cd` to root and set `PYTHONPATH`).

- **No module named tests.smoke_retrieval**  
  Use `win_scripts\smoke.bat` (which calls the file directly), or add `tests/__init__.py` to enable `-m` style.

- **Virtualenv not found / wrong interpreter**  
  Always activate with `call .venv\Scripts\activate.bat`.  
  If multiple Python versions exist, ensure `py -3` creates the venv in `win_scripts\install.bat` (already handled).

- **ChromaDB lock or permission errors**  
  Stop other processes using the DB and delete the lock file under `CHROMA_DIR`.  
  Ensure `CHROMA_DIR` points to a writeable location.

- **Model/Quota errors**  
  Verify `CHAT_MODEL` and `EMBEDDING_MODEL` names are available to your API key.  
  Check your OpenAI usage limits.

## Security Notes

- Never commit API keys to source control.
- Prefer environment variables over hardcoding.
- If you distribute an EXE, it should not embed your key; use a wrapper `.bat` or instruct users to set their own `OPENAI_API_KEY`.

------------------------------------------------
Enjoy your reading journey with Smart Librarian!
