import os
import platform
import shutil
import csv


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
    """
    Appends a formatted message to the output list and triggers a repaint of the output component.

    Args:
        output (list): The list or object to which the message will be appended.
        message (str): The message to append and print.
    
    Returns:
        None
    """
    output.append(f"<b>{message}</b> \n")
    output.repaint()
    # Print the message to the console
    print(message)


# Function to convert a CSV file to JSON
def csv_to_json(csv_file_path):
    """
    Converts a CSV file to a JSON format.

    Args:
        csv_file_path (str): The path to the CSV file to be converted.

    Returns:
        list: A list of dictionaries representing the CSV data in JSON format.
    """
    json_data = []
    with open(csv_file_path, "r", newline="", encoding="utf-8-sig") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Remove any unwanted characters from keys
            clean_row = {
                key.strip("\ufeff").strip('"'): value for key, value in row.items()
            }
            json_data.append(clean_row)
    return json_data


def convet_into_csv_and_save(json_data, out_put_csv):
    """
    Converts JSON data to CSV format and saves it to a specified file.

    Args:
        json_data (list or dict): The JSON data to be converted, either as a dictionary or a list of dictionaries.
        out_put_csv (str): The path to the output CSV file.

    Raises:
        ValueError: If the input json_data is not a dictionary or a list of dictionaries.

    Returns:
        None
    """
    # Ensure json_data is iterable
    if isinstance(json_data, dict):
        json_data = [
            json_data
        ]  # Convert single dictionary to a list containing that dictionary
    elif not isinstance(json_data, list):
        raise ValueError(
            "Input json_data should be a dictionary or a list of dictionaries."
        )

    report_directory = os.path.dirname(out_put_csv)
    print("report_directory", report_directory)

    if not os.path.exists(report_directory):
        os.makedirs(report_directory)
        print(f"Created directory: {report_directory}")

    with open(out_put_csv, "w", newline="") as file:
        writer = csv.writer(file)

        # Write header using keys from the first dictionary in the JSON data
        writer.writerow(json_data[0].keys())

        # Write rows
        for row in json_data:
            writer.writerow(row.values())
