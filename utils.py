"""
This script provides utility functions and configurations for a PyQt-based GUI application. 
Modules:
    - os: Provides functions for interacting with the operating system.
    - platform: Provides a way to access underlying platform’s data.
    - shutil: Provides functions to operate on files and collections of files.
    - csv: Provides functionality to read and write CSV files.
    - json: Provides methods for parsing and creating JSON data.
    - PyQt5.QtWidgets.QDesktopWidget: Provides screen-related information and utilities.
    - PyQt5.QtWidgets.QMessageBox: Provides a dialog box to display messages to the user.
"""
import os
import platform
import shutil
import csv
import json
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QMessageBox
# Additional code and function definitions go here

def ensure_log_folder_exists(folder_path):
    """
    Ensure that the specified log folder exists. If it doesn't exist, create it.

    Args:
        folder_path (str): The path to the log folder.

    Returns:
        None
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created log folder: {folder_path}")
    else:
        print(f"Log folder already exists: {folder_path}")
def show_message_box(parent, icon_type, title, text):
    """
    Display a message box with specified icon, title, and text.

    Args:
        parent (QWidget or None): Parent widget of the message box.
        icon_type (QMessageBox.Icon): Icon type to display (e.g., QMessageBox.Information, QMessageBox.Question).
        title (str): Title of the message box.
        text (str): Text content of the message box.

    Returns:
        StandardButton: Button clicked by the user (QMessageBox.Yes or QMessageBox.No for question icon, QMessageBox.Ok for other icons).
    """
    msg_box = QMessageBox(parent)
    msg_box.setIcon(icon_type)
    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    # Set standard buttons based on icon_type using a ternary operator
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No) if icon_type == QMessageBox.Question else msg_box.setStandardButtons(QMessageBox.Ok)
    return msg_box.exec_()



def center_window(window):
    """
    Center the given PyQt window on the screen.

    Args:
        window (QWidget): The PyQt window to be centered.
    """
    qr = window.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    window.move(qr.topLeft())



def find_chrome_path():
    """
    Finds the path to the Google Chrome executable on the system.

    Returns:
        str: The path to the Chrome executable if found, otherwise None.
    """
    system = platform.system()  # Get the current operating system
    print(f"system : {system}")
    # Handle Windows systems
    if system == "Windows":
        # Possible paths for Chrome on Windows
        chrome_paths = [
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Google", "Chrome", "Application", "chrome.exe"),
        ]
        # Check if Chrome exists at any of these paths
        return next((path for path in chrome_paths if os.path.exists(path)), None)
    # Handle Linux systems
    elif system == "Linux":
        # Try to find Chrome using `shutil.which`
        return shutil.which("google-chrome") or shutil.which("google-chrome-stable")
    # Return None if Chrome is not found
    return None


async def page_load(page, pageurl):
    """
    Loads a web page asynchronously using Puppeteer and checks the response status.
    Parameters:
    - page: Puppeteer page object.
    - pageurl (str): Base URL for the web page.
    Returns:
    - bool: True if page loaded successfully, False otherwise.
    """
    # Navigate to the page and wait for DOM content to be loaded
    response = await page.goto(pageurl, waitUntil="domcontentloaded")
    # Check response status using ternary operators
    return False if response.status in [404, 403] else True


def print_the_output_statement(output, message):
    """
    Appends a formatted message to the output list and triggers a repaint of the output component.

    Args:
        output (list): The list or object to which the message will be appended.
        message (str): The message to append and print.

    Returns:
        None
    """
    output.append(f"<b>{message}</b> \n \n")
    output.repaint()
    # Print the message to the console
    print(message)


# Function to convert a CSV file to JSON
def csv_to_json(csv_file):
    """
    Converts a CSV file to a JSON formatted string and retrieves the headers.

    Args:
        csv_file (str): The path to the CSV file to be converted.

    Returns:
        tuple: A tuple containing:
            - list: A list of strings representing the headers (field names) extracted from the CSV file.
            - str: A JSON formatted string representing the CSV data with an indentation of 4 spaces.

            If an error occurs during file handling or JSON conversion:
            - (None, str): (None, "Error: The specified CSV file was not found.") if the CSV file is not found.
            - (None, str): (None, f"Error: An unexpected error occurred - {error_message}") for other errors.
    """
    try:
        json_data = []
        # Open the CSV file with UTF-8-sig encoding to handle BOM (Byte Order Mark)
        with open(csv_file, "r", newline="", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)  # Create a CSV reader object
            headers = reader.fieldnames  # Retrieve the headers from the CSV
            for row in reader:
                json_data.append(row)  # Append each row (dictionary) to json_data list

        # Convert json_data list to a formatted JSON string
        json_data_str = json.dumps(json_data, indent=4)

        # Return headers and JSON formatted string
        return headers, json_data_str

    except FileNotFoundError:
        return None, "Error: The specified CSV file was not found."

    except Exception as e:
        # Handle unexpected errors by returning None for headers and an error message
        return None, f"Error: An unexpected error occurred - {str(e)}"


def convert_into_csv_and_save(json_data, out_put_csv):
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

    ensure_log_folder_exists(report_directory)
    
    with open(out_put_csv, "w", newline="") as file:
        writer = csv.writer(file)

        # Write header using keys from the first dictionary in the JSON data
        writer.writerow(json_data[0].keys())

        # Write rows
        for row in json_data:
            writer.writerow(row.values())


def check_json_length(json_data):
    """
    Returns the length of a JSON object (dict or list).
    Args:
        json_data (str or dict): JSON string or parsed JSON object.

    Returns:
        int: Length of the JSON object, or -1 if invalid.
    """
    try:
        if isinstance(json_data, str):
            json_obj = json.loads(json_data)
        elif isinstance(json_data, dict):
            json_obj = json_data
        else:
            return -1

        if isinstance(json_obj, (list, dict)):
            return len(json_obj)
        else:
            return -1

    except ValueError as e:
        print(f"ValueError: {e}")
        return -1



def load_stylesheet(file_path):
    """
    Loads and returns the contents of a stylesheet file.

    Args:
        file_path (str): Path to the stylesheet file.

    Returns:
        str: The contents of the stylesheet file.
    """
    with open(file_path, "r") as file:
        stylesheet = file.read()
    return stylesheet


