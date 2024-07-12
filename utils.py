import os
import platform
import shutil
import csv
import json


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


def print_the_output_statement(output, message):
    output.append(message)
    output.repaint()
    # Print the message to the console
    print(message)


# Function to convert a CSV file to JSON
def csv_to_json(csv_file_path):
    json_data = []

    with open(csv_file_path, 'r', newline='', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Remove any unwanted characters from keys
            clean_row = {key.strip('\ufeff').strip('"'): value for key, value in row.items()}
            json_data.append(clean_row)
    return json_data
