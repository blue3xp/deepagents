# DeepAgents Code CLI

A specialized CLI tool for autonomous feature implementation in existing codebases using DeepAgents.

## Overview

`deepagents-code-cli` is designed to add new features to a codebase without user intervention. It uses an AI agent equipped with coding skills to:
1.  Analyze the existing codebase.
2.  Plan the implementation.
3.  Write the code.
4.  Write and run unit tests.
5.  Verify the implementation before completion.

## Installation

```bash
pip install deepagents-code-cli
```

## Configuration

Create a `.env` file in your working directory (or set environment variables):

```env
CODEBASE_PATH=/path/to/your/codebase
FEATURE_DESCRIPTION="Description of the feature you want to implement."
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key (optional)
MODEL_NAME=gpt-4o (optional, defaults to gpt-4o)
```

## Usage

```bash
deepagents-code-cli
```

The agent will start working on the feature described in `.env`. It will analyze the code in `CODEBASE_PATH`, implement the feature, and verify it with tests.

## Development

This package depends on `deepagents-cli` and `deepagents` libraries.

```bash
# Install dependencies
pip install -e .
```
