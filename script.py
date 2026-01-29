import re
import os
import subprocess
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
    with sync_playwright() as playwright:
        repo_name = "Intelligent-Github-Automation"
        visibility = "public"
        repo_link = run(playwright, repo_name, visibility)
        
        if repo_link:
            print("\nRunning setup_repo.sh...")
            subprocess.run(["./setup_repo.sh", repo_link])


