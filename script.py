import re
import os
import subprocess
import argparse
from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright, expect

# Load environment variables from .env file
load_dotenv()

def run(playwright: Playwright, repo_name: str, visibility: str = "public") -> str | None:
    # Launch browser - headless=False so you can see the magic happen
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # 1. Login to GitHub
    page.goto("https://github.com/login")
    
    # Fill credentials from .env
    username = os.getenv("GITHUB_USERNAME")
    password = os.getenv("GITHUB_PASSWORD")
    
    if not username or not password:
        print("Error: GITHUB_USERNAME or GITHUB_PASSWORD not found in .env file.")
        return None

    page.get_by_role("textbox", name="Username or email address").fill(username)
    page.get_by_role("textbox", name="Password").fill(password)
    page.get_by_role("button", name="Sign in", exact=True).click()

    # 2. Open the New Repository page (Direct Navigation)
    # Navigating directly is more reliable than clicking the dropdown menu
    page.goto("https://github.com/new")

    # 3. Create the repository
    print(f"Attempting to create repository: {repo_name} ({visibility})")
    
    page.get_by_role("textbox", name="Repository name *").fill(repo_name)

    # Select Visibility
    if visibility.lower() == "private":
        page.get_by_role("button", name="Public").click()
        page.get_by_text("Private", exact=True).click()
    
    # Wait for GitHub to validate the name and enable the button
    # The button is at the bottom, so we find it by text and ensure it's the submit button
    create_button = page.get_by_role("button", name="Create repository")
    
    # Wait for the validation message to appear
    # This matches the text seen in the screenshot: "auto-repo-... is available."
    expect(page.get_by_text(f"{repo_name} is available.")).to_be_visible()
    
    # Ensure button is enabled
    expect(create_button).to_be_enabled()
    
    # Scroll into view and click forcefully
    create_button.scroll_into_view_if_needed()
    create_button.click(force=True)

    # 4. Verify Success
    # GitHub redirects to the new repo main page
    expect(page).to_have_url(re.compile(repo_name), timeout=30000)
    repo_link = f"git@github.com:{username}/{repo_name}.git"
    print(f"Successfully created repository: {repo_link}")

    # Clean up
    context.close()
    browser.close()
    
    return repo_link

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a GitHub repository using Playwright.")
    parser.add_argument("repo_name", help="The name of the repository to create.")
    parser.add_argument("--visibility", choices=["public", "private"], default="public", help="The visibility of the repository (default: public).")
    args = parser.parse_args()

    with sync_playwright() as playwright:
        repo_link = run(playwright, args.repo_name, args.visibility)
        
        if repo_link:
            print("\nRunning setup_repo.sh...")
            # Get the directory where script.py is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            setup_script_path = os.path.join(script_dir, "setup_repo.sh")
            
            subprocess.run([setup_script_path, repo_link])


