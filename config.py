from datetime import datetime
import os
from screeninfo import get_monitors

# Apps COnfigrations
# Constants for file naming and paths Save data
APP_NAME = "abcbiz_report"

APP_BUTTON_NAME = "Login"


REPORT_FOLDER = "Daily_Report"
FILE_TYPE = "csv"
CURRENT_DATE = datetime.now()
FILE_NAME = "ABCGovtWebscrapping"


LOGINURL = "https://abcbiz.abc.ca.gov/login"  # URL for licensing reports


# Headless
HEADLESS = True  # Whether to run the app in headless mode (no GUI)
# Screem COnfig
WIDTH = get_monitors()[0].width
HEIGHT = get_monitors()[0].height


# Ensure the log folder exists
log_folder = "log"
os.makedirs(log_folder, exist_ok=True)


# Function to write log entries directly to a file
def log_entry(log_type, service_id, name, status):
    # Define the log file name within the log folder
    log_filename = os.path.join(log_folder, f"logfile_{CURRENT_DATE.strftime("%Y-%m-%d")}.txt")

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
