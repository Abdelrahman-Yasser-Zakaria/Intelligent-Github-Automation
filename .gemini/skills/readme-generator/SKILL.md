---
name: readme-generator
description: Generates a README.md file for the current project. Use when the user types /readme or asks to create/generate a readme.
---

# Readme Generator

## Overview

This skill generates a comprehensive `README.md` file for the current project by analyzing the codebase.

## Workflow

1.  **Analyze the Codebase**:
    *   List files in the current directory to understand the project structure.
    *   Identify the project type (e.g., Python, Node.js, Shell script).
    *   Read key files (e.g., `main` scripts, `package.json`, `setup.py`, `requirements.txt`) to understand functionality.

2.  **Generate Content**:
    Create a `README.md` file with the following sections:
    *   **# Project Title**: Inferred from the directory name or main script.
    *   **Description**: A clear summary of what the project does.
    *   **Prerequisites**: Tools or libraries required (e.g., Python 3.x, Playwright, Node.js).
    *   **Installation**: Steps to set up the environment (e.g., `pip install -r requirements.txt`, `npm install`).
    *   **Usage**: How to run the project (e.g., `python script.py`, `./setup_repo.sh`).
    *   **Features**: Bullet points of key capabilities.

3.  **Write File**:
    *   Use the `write_file` tool to save the content to `README.md`.
    *   If `README.md` already exists, ask the user before overwriting, or create `README_NEW.md`.