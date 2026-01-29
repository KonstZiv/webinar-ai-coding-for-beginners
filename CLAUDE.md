# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python project for a webinar about AI-assisted coding for beginners. Uses the `tic-tac-toe-3x3` library with `rich` for terminal UI.

## Commands

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Run a single test file
uv run pytest tests/test_example.py

# Run a specific test
uv run pytest tests/test_example.py::test_function_name

# Lint code
uv run ruff check .

# Format code
uv run ruff format .

# Fix linting issues automatically
uv run ruff check . --fix
```

## Architecture

- `src/my-tic-tac-toe/` - Main application source code
- `tests/` - Test files (pytest)

## Tech Stack

- Python 3.14+
- `uv` - Dependency and virtual environment management
- `pytest` - Testing framework
- `ruff` - Linting and formatting
- `rich` - Terminal UI library
- `tic-tac-toe-3x3` - Game logic library
