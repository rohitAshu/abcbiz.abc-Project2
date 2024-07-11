import os
import platform
import shutil


def find_chrome_path():
    """
    Finds the path to the Google Chrome executable on the system.

    Returns:
        str: The path to the Chrome executable if found, otherwise None.
    """
    # Get the current operating system
    system = platform.system()
    print(f"system : {system}")

    # Handle Windows systems
    if system == "Windows":
        # Possible paths for Chrome on Windows
        chrome_paths = [
            os.path.join(
                os.environ["ProgramFiles"],
                "Google",
                "Chrome",
                "Application",
                "chrome.exe",
            ),
            os.path.join(
                os.environ["ProgramFiles(x86)"],
                "Google",
                "Chrome",
                "Application",
                "chrome.exe",
            ),
        ]
        # Check if Chrome exists at any of these paths
        for path in chrome_paths:
            if os.path.exists(path):
                return path

    # Handle Linux systems
    elif system == "Linux":
        # Try to find Chrome using `shutil.which`
        chrome_path = shutil.which("google-chrome")
        if chrome_path is None:
            # Fallback to a stable version if the default one isn't found
            chrome_path = shutil.which("google-chrome-stable")
        return chrome_path

    # Return None if Chrome is not found
    return None


async def page_load(page, pageurl):
    """
    Loads a web page asynchronously using Puppeteer and checks the response status.

    Parameters:
    - page: Puppeteer page object.
    - date (str): Date parameter to include in the URL query.
    - pageurl (str): Base URL for the web page.

    Returns:
    - bool: True if page loaded successfully, False otherwise.
    """
    print(f"Opening page from URL: {pageurl}")
    # Navigate to the page and wait for DOM content to be loaded
    response = await page.goto(pageurl, waitUntil="domcontentloaded")
    # Check response status
    if response.status == 404:
        print(f"Page not found: {pageurl}")
        return False
    elif response.status == 403:
        print("403 Forbidden")
        return False
    else:
        return True


async def check_condition(page):
    check_script = """
    function checkCondition() {
        const div = document.querySelector('div.sc-gAnuJb.gzDMq');
        if (div) {
            const pElement = div.querySelector('p');
            if (pElement && pElement.textContent.trim() === "There are no records by selected search parameters") {
                return true;
            }
        }
        return false;
    }
    checkCondition();
    """
    condition_exists = await page.evaluate(check_script)
    return condition_exists