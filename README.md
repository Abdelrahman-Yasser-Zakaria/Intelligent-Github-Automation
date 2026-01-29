# Intelligent GitHub Automation

This project provides an automated workflow for creating a new GitHub repository and setting up your local directory as a Git repository linked to that new remote. It uses **Playwright** for browser automation and a **Bash script** for Git operations.

## Features

- **Automated GitHub Repository Creation**: Logs into GitHub, navigates to the "New Repository" page, and creates a repo with a specified name and visibility.
- **Dynamic Visibility**: Support for both `Public` and `Private` repositories.
- **Smart Git Setup**: A shell script (`setup_repo.sh`) that:
  - Detects if the current directory is already a Git repository.
  - Initializes a new Git repository if necessary.
  - Adds the newly created GitHub repository as the `origin` remote.
  - Handles branching (renames to `main`) and pushes the initial commit.
- **Gemini CLI Integration**: Optionally generates a `README.md` using the Gemini CLI if one doesn't exist.

## Prerequisites

- **Python 3.x**
- **Playwright**: For browser automation.
- **python-dotenv**: To manage environment variables.
- **Git**: For version control operations.
- **Bash**: To run the setup script.

## Installation

1. **Clone the repository** (or copy the scripts into your project):
   ```bash
   git clone <this-repo-url>
   cd Github-Automation
   ```

2. **Install Python dependencies**:
   ```bash
   pip install playwright python-dotenv
   playwright install chromium
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory and add your GitHub credentials:
   ```env
   GITHUB_USERNAME=your_username
   GITHUB_PASSWORD=your_password
   ```

## Usage

### 1. Automated Flow (Python Script)
Run the main Python script to create a repository on GitHub and automatically trigger the local setup:

```bash
python script.py
```
*Note: You can modify the `repo_name` and `visibility` variables in the `if __name__ == "__main__":` block of `script.py`.*

### 2. Manual Git Setup (Shell Script)
If you already have a GitHub repository URL and just want to automate the local linking/pushing:

```bash
chmod +x setup_repo.sh
./setup_repo.sh <YOUR_GITHUB_REPO_URL>
```

## Project Structure

- `script.py`: The Playwright automation script for creating repositories.
- `setup_repo.sh`: The bash script for Git initialization and remote setup.
- `.env`: (User-created) Stores sensitive GitHub credentials.
- `AI/`: Contains learning materials and prompts used during development.

## Development Note

This project was developed with the assistance of **Gemini CLI**, leveraging automated browser interactions and shell scripting to streamline the "New Project" workflow.
