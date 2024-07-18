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
import pandas as pd
import numpy as np






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
    (
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if icon_type == QMessageBox.Question
        else msg_box.setStandardButtons(QMessageBox.Ok)
    )
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
    system = platform.system()
    print(f"System: {system}")

    # Handle Windows systems
    if system == "Windows":
        possible_paths = [
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Google", "Chrome", "Application", "chrome.exe"),
        ]

        # Windows 10 and 11 might have additional installation paths
        windows_specific_paths = [
            os.path.join(os.environ.get("LOCALAPPDATA", "C:\\Users\\%USERNAME%\\AppData\\Local"), "Google\\Chrome\\Application\\chrome.exe"),
            os.path.join(os.environ.get("APPDATA", "C:\\Users\\%USERNAME%\\AppData\\Roaming"), "Google\\Chrome\\Application\\chrome.exe"),
        ]
        possible_paths.extend(windows_specific_paths)

        # Check if Chrome exists at any of these paths
        chrome_path = next((path for path in possible_paths if os.path.exists(path)), None)
        
        # Example temporary directory (adjust according to your use case)
        temp_dir = os.path.join(os.environ.get("TEMP", "C:\\Temp"), "chrome_temp")

        # Clean up the temporary directory
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        except OSError as e:
            print(f"Error: {e.strerror}")

        return chrome_path

    # Handle Linux systems (Ubuntu)
    elif system == "Linux":
        chrome_path = shutil.which("google-chrome") or shutil.which("google-chrome-stable")
        if chrome_path:
            return chrome_path

        # Additional common paths for Chrome on Ubuntu
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
    Loads a web page asynchronously using Puppeteer and checks the response status.
    Parameters:
    - page: Puppeteer page object.
    - pageurl (str): Base URL for the web page.
    Returns:
    - bool: True if page loaded successfully, False otherwise.
    """
    # Navigate to the page and wait for DOM content to be loaded
    response = await page.goto(pageurl, waitUntil="domcontentloaded")
    print(response)
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
    # Print the message to the console
    print(message)


def convert_into_csv_and_save(json_data, out_put_csv):
    


    report_directory = os.path.dirname(out_put_csv)
    print("report_directory", report_directory)

    ensure_log_folder_exists(report_directory)
    print(json_data)
    df = pd.DataFrame(json_data)
    df.to_csv(out_put_csv, index=False)  # Set index=False to exclude DataFrame index in the CSV output
    print(f'json to csv converted successfully with the {out_put_csv} ')

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


# Additional code and function definitions go here

def xlsx_to_json(xlsx_file_path):
    # Load Excel file
    df = pd.read_excel(xlsx_file_path)
    
    # Clean and convert specific columns to integers (if needed)
    numeric_columns = ['Server_ID']  # Specify columns that should be numeric
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    
    # Get header columns
    header_columns = list(df.columns)
    num_records = len(df.index)
    
    # Convert DataFrame to JSON
    json_data = df.to_json(orient='records', force_ascii=False)
    
    return header_columns, json_data, num_records