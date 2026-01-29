#!/bin/bash

# Check if a Github repository URL is provided
if [ -z "$1" ]; then
  echo "Error: Please provide the GitHub repository URL."
  echo "Usage: ./setup_repo.sh <REPO_URL>"
  exit 1
fi

REPO_URL=$1

echo "Checking git status..."

# Check if the current directory is already a git repository
if git status > /dev/null 2>&1; then
  echo "Current directory is already a git repository."
  
  # Check if remote 'origin' already exists
  if git remote | grep -q "^origin$"; then
    echo "Remote 'origin' already exists. Updating URL..."
    git remote set-url origin "$REPO_URL"
  else
    echo "Adding remote 'origin'..."
    git remote add origin "$REPO_URL"
  fi

  echo "Renaming branch to 'main'..."
  git branch -M main

  echo "Pushing to GitHub..."
  git push -u origin main

else
  echo "Current directory is NOT a git repository. Initializing..."

  echo "Initializing git..."
  git init

  # Generate README.md using Gemini CLI
  if [ ! -f "README.md" ]; then
    echo "Generating README.md with Gemini CLI..."
    gemini "/readme" --yolo
  fi

  echo "Adding files..."
  git add .

  echo "Committing..."
  git commit -m "first commit"

  echo "Renaming branch to 'main'..."
  git branch -M main

  echo "Adding remote origin..."
  git remote add origin "$REPO_URL"

  echo "Pushing to GitHub..."
  git push -u origin main
fi

echo "Done!"
