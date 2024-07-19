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

import json
import os
import platform
import shutil
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QMessageBox
import pandas as pd

def create_directory(folder_path):
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
    (
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if icon_type == QMessageBox.Question
        else msg_box.setStandardButtons(QMessageBox.Ok)
    )
    return msg_box.exec_()


def center_window(window):
    """
    Centers the given window on the screen.

    Args:
        window (QWidget): The PyQt widget (e.g., QMainWindow) that needs to be centered.

    Returns:
        None

    Notes:
        - This function adjusts the position of the provided window so that it is centered on the available screen area.
        - It uses the available geometry of the screen to ensure the window is centered correctly, accounting for taskbars and other screen elements.
    """
    # Get the geometry of the window frame
    qr = window.frameGeometry()

    # Get the center point of the available screen area
    cp = QDesktopWidget().availableGeometry().center()

    # Move the center of the window frame to the center of the screen
    qr.moveCenter(cp)

    # Move the top-left corner of the window frame to the new position
    window.move(qr.topLeft())


def find_chrome_path():
    """
    Finds the installation path of Google Chrome based on the operating system.

    Returns:
        str: The path to the Chrome executable if found; otherwise, `None`.

    Notes:
        - On Windows, the function checks common installation paths and handles different system environments.
        - On Linux, the function checks standard locations and uses `shutil.which` to find `google-chrome` or `google-chrome-stable`.
        - A temporary directory is cleaned up as part of the process, if it exists.

    Raises:
        OSError: If there is an issue cleaning up the temporary directory.
    """
    system = platform.system()
    print(f"System: {system}")

    if system == "Windows":
        # Define possible installation paths for Chrome
        possible_paths = [
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Google", "Chrome", "Application", "chrome.exe"),
        ]

        # Add additional common paths for Windows 10 and 11
        windows_specific_paths = [
            os.path.join(os.environ.get("LOCALAPPDATA", "C:\\Users\\%USERNAME%\\AppData\\Local"), "Google\\Chrome\\Application\\chrome.exe"),
            os.path.join(os.environ.get("APPDATA", "C:\\Users\\%USERNAME%\\AppData\\Roaming"), "Google\\Chrome\\Application\\chrome.exe"),
        ]
        possible_paths.extend(windows_specific_paths)

        # Find the first valid Chrome path
        chrome_path = next((path for path in possible_paths if os.path.exists(path)), None)

        # Temporary directory cleanup
        temp_dir = os.path.join(os.environ.get("TEMP", "C:\\Temp"), "chrome_temp")
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        except OSError as e:
            print(f"Error: {e.strerror}")

        return chrome_path

    elif system == "Linux":
        # Try to find Chrome using `shutil.which`
        chrome_path = shutil.which("google-chrome") or shutil.which("google-chrome-stable")
        if chrome_path:
            return chrome_path

        # Additional common paths for Chrome on Linux
        linux_specific_paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/opt/google/chrome/google-chrome",
        ]
        return next((path for path in linux_specific_paths if os.path.exists(path)), None)

    # Return None if Chrome is not found
    return None


async def page_load(page, pageurl):
    """
    Navigates to a specified URL and waits for the DOM content to be loaded.

    Args:
        page (pyppeteer.page.Page): The Pyppeteer Page object used to interact with the web page.
        pageurl (str): The URL of the page to navigate to.

    Returns:
        bool: `True` if the page loaded successfully (response status is not 404 or 403); `False` otherwise.

    Raises:
        ValueError: If the response status is 404 (Not Found) or 403 (Forbidden).
    
    Notes:
        - The function uses `page.goto` to navigate to the specified URL and waits until the DOM content is fully loaded.
        - The response status is checked to determine if the page loaded successfully. If the status is 404 or 403, the function returns `False`.
    """
    # Navigate to the page and wait for DOM content to be loaded
    response = await page.goto(pageurl, waitUntil="domcontentloaded")
    
    # Print the response for debugging purposes
    print(response)
    
    # Check response status and return result
    return False if response.status in [404, 403] else True



def print_the_output_statement(output, message):
    """
    Appends a formatted message to a QTextEdit widget and prints the message to the console.

    Args:
        output (QTextEdit): The QTextEdit widget where the message will be appended.
        message (str): The message to be formatted and added to the QTextEdit widget, and printed to the console.

    Returns:
        None
    Notes:
        - The message is appended to the `output` widget with bold formatting.
        - The message is also printed to the console for debugging or logging purposes.
    """
    # Append the formatted message to the QTextEdit widget
    output.append(f"<b>{message}</b>\n\n")

    # Print the message to the console
    print(message)



def convert_into_csv_and_save(json_data, out_put_csv):
    """
    Converts JSON data to a CSV file and saves it to the specified output path.

    Args:
        json_data (list of dict): The JSON data to be converted. It should be a list of dictionaries where each dictionary represents a row.
        out_put_csv (str): The path to the output CSV file where the data will be saved.

    Returns:
        None

    Raises:
        ValueError: If the provided JSON data is not in the expected format (a list of dictionaries).
        IOError: If there is an issue creating the directory or saving the CSV file.
    """
    # Extract the directory from the output file path
    report_directory = os.path.dirname(out_put_csv)
    print("Report directory:", report_directory)

    # Create the directory if it does not exist
    create_directory(report_directory)

    # Check the format of the JSON data
    if not isinstance(json_data, list) or not all(isinstance(item, dict) for item in json_data):
        raise ValueError("JSON data must be a list of dictionaries.")

    # Convert JSON data to a DataFrame
    df = pd.DataFrame(json_data)
    
    try:
        # Save the DataFrame to a CSV file
        df.to_csv(out_put_csv, index=False)  # Exclude DataFrame index from CSV output
        print(f'JSON data successfully converted to CSV and saved to {out_put_csv}')
    except IOError:
        raise IOError(f"An error occurred while creating the file or saving data to '{out_put_csv}'.")




def load_stylesheet(file_path):
    """
    Loads a stylesheet from a specified file.

    Args:
        file_path (str): The path to the stylesheet file to be loaded.

    Returns:
        str: The contents of the stylesheet file as a string.

    Raises:
        FileNotFoundError: If the specified stylesheet file does not exist.
        IOError: If there is an issue reading the file.
    """
    try:
        with open(file_path, "r") as file:
            stylesheet = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at path '{file_path}' does not exist.")
    except IOError:
        raise IOError(f"An error occurred while reading the file at '{file_path}'.")

    return stylesheet


# Additional code and function definitions go here

def xlsx_to_json(xlsx_file_path):
    """
    Converts an Excel file to a JSON string and provides metadata about the data.

    Args:
        xlsx_file_path (str): The path to the Excel file to be converted.
    Returns:
        tuple:
            - header_columns (list of str): A list of column headers from the Excel file.
            - json_data (str): A JSON-formatted string representing the contents of the Excel file.
            - num_records (int): The total number of records (rows) in the Excel file.
    Raises:
        FileNotFoundError: If the specified Excel file does not exist.
        ValueError: If there is an issue reading the Excel file.
    """
    # Read the Excel file
    df = pd.read_excel(xlsx_file_path)
    
    # Convert the DataFrame to a dictionary
    data_dict = df.to_dict(orient='records')
    
    # Convert the dictionary to a JSON string
    json_data = json.dumps(data_dict, indent=4)
    
    # Get the total number of rows
    num_records = len(df)
    
    # Get the list of headers
    header_columns = list(df.columns)
    
    return header_columns, json_data, num_records
