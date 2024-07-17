import os
from datetime import datetime
from screeninfo import get_monitors

from utils import ensure_log_folder_exists

# Constants used throughout the application
APP_NAME = "ABC Business Online Portal"  # Name of the application
APP_BUTTON_NAME = "Login"  # Name of the login button
REPORT_FOLDER = "Daily_Report"  # Folder where reports are stored
FILE_TYPE = "csv"  # Type of the report files
CURRENT_DATE = datetime.now()  # Current date and time
FILE_NAME = "ABCGovtWebscrapping"  # Base name for the files
LOG_TYPE = "log"  # Type of log files
LOG_FOLDER = "log"  # Folder where log files are stored
LOGINURL = "https://abcbiz.abc.ca.gov/login"  # URL for the login page
HEADLESS = True  # Flag for headless browser mode

# Get the width and height of the primary monitor
monitor = get_monitors()[0]
WIDTH = monitor.width  # Width of the screen
HEIGHT = monitor.height  # Height of the screen

ensure_log_folder_exists(LOG_FOLDER)


# Function to write log entries directly to a file
def log_entry(log_type, service_id, name, status):
    # Define the log file name within the log folder
    log_filename = os.path.join(
        LOG_FOLDER, f"logfile_{CURRENT_DATE.strftime('%Y-%m-%d_%H-%M-%S')}.{LOG_TYPE}"
    )
    # Check if the file already exists to write the header only once
    file_exists = os.path.isfile(log_filename)

    # Create the log entry
    log_entry = f"{CURRENT_DATE.strftime('%Y-%m-%d %H:%M:%S')}, {log_type}, {service_id}, {name}, {status}\n"

    # Write the log entry to the file
    with open(log_filename, "a") as log_file:
        if not file_exists:
            # Write the header if the file does not exist
            log_file.write("Reported Date, ServiceID, Name, Status\n")
        log_file.write(log_entry)
