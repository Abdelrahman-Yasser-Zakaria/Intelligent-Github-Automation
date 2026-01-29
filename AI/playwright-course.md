Here is your crash course on **Playwright for Python**.

Playwright is a modern automation library from Microsoft that is faster, more reliable, and easier to use than Selenium. It supports **Chromium** (Chrome, Edge), **Firefox**, and **WebKit** (Safari).

### 1. Installation
Install the Python package and the required browser binaries.
```bash
pip install playwright
playwright install
```

### 2. The "Magic" Tool: Codegen
The fastest way to learn is to let Playwright write the code for you.
Run this command to open a browser that records your clicks and typing:
```bash
playwright codegen github.com
```
*   It opens a browser window and an "Inspector" window.
*   Perform your actions (login, click "New", etc.).
*   Copy the generated Python code from the Inspector window.

### 3. Core Concepts

#### **A. Sync vs. Async**
Playwright works in two modes.
*   **Sync:** Easier for simple scripts and learning (blocks until action completes).
*   **Async:** Better for high-performance apps or when integrating with `asyncio`.

**Basic Sync Script:**
```python
from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    # 1. Launch Browser (headless=False lets you see it happen)
    browser = p.chromium.launch(headless=False)
    
    # 2. Create a Context (like a fresh incognito profile)
    context = browser.new_context()
    
    # 3. Open a Page (Tab)
    page = context.new_page()
    
    # 4. Navigate
    page.goto("https://github.com/login")
    
    # 5. Interact & Assert
    page.get_by_label("Username").fill("my_username")
    page.get_by_label("Password").fill("my_password")
    page.get_by_role("button", name="Sign in").click()
    
    # Wait automatically for the next page to load
    expect(page.get_by_role("link", name="Create new")).to_be_visible()
    
    browser.close()
```

#### **B. Locators (Finding Elements)**
Playwright encourages **user-facing locators** (how a real user finds things), not XPaths or CSS IDs.
*   `page.get_by_role("button", name="Submit")` (Best practice)
*   `page.get_by_label("Password")` (Great for forms)
*   `page.get_by_text("Welcome")`
*   `page.get_by_placeholder("Search")`

#### **C. Actions**
Playwright **auto-waits** for elements to be actionable (visible, not covered, enabled). You rarely need `time.sleep()`.
*   `.click()`
*   `.fill("text")`
*   `.check()` / `.uncheck()`
*   `.select_option("value")`

#### **D. Assertions**
Use `expect` to verify state. It has auto-retrying logic (it waits ~5s for the condition to become true before failing).
```python
from playwright.sync_api import expect

# Check if visible
expect(page.get_by_text("Success")).to_be_visible()

# Check URL
expect(page).to_have_url("https://github.com/")

# Check value
expect(page.locator("#search")).to_have_value("Playwright")
```

### 4. Tracing (Debugging)
If a test fails, you can record a "Trace" which is a time-travel debugging tool. It captures screenshots, network logs, and DOM snapshots for every step.

```python
context.tracing.start(screenshots=True, snapshots=True)
# ... run your actions ...
context.tracing.stop(path="trace.zip")
```
View it at [trace.playwright.dev](https://trace.playwright.dev) or run `playwright show-trace trace.zip`.

### Summary Checklist for Your Task
1.  **Install:** `pip install playwright && playwright install`
2.  **Record:** Run `playwright codegen github.com/login`
3.  **Refine:** Clean up the generated code (remove cookies/unnecessary clicks).
4.  **Run:** Execute your Python script.

Ready to start? I can generate the script for you now.