import asyncio
import os
from datetime import datetime
from screeninfo import get_monitors
import time
from utils import create_directory
from threading import Event


# Configuration settings for the ABC Business Online Portal application.

# Application Settings
APP_TITLE = "ABC Business Online Portal"
# Title of the application window

APP_NAME = "ABC Business Online Portal"
# Name displayed in the application, used in the UI

APP_BUTTON_NAME = "Login"
# Label for the login button in the application

# Report Settings
REPORT_FOLDER = "Daily_Report"
# Directory name for saving daily report files

FILE_TYPE = "csv"
# File extension for the report files

CURRENT_DATE = datetime.now()
# Current date and time used for generating timestamped reports

FILE_NAME = "ABCGovtWebscrapping"
# Base name for the report files

LOG_TYPE = "log"
# File extension for log files

LOG_FOLDER = "log"
# Directory name for saving log files

# Web Scraping Settings
LOGINURL = "https://abcbiz.abc.ca.gov/login"
# URL for the login page of the web portal

HEADLESS = True
# Boolean indicating whether to run the browser in headless mode (i.e., without a GUI)

# Display Settings
monitor = get_monitors()[0]
# The primary monitor's display information

WIDTH = monitor.width
# Width of the primary monitor

HEIGHT = monitor.height
# Height of the primary monitor

# Thread and Event Settings
THREAD_EVENT = Event()
# Event object used for thread synchronization

NEW_EVENT_LOOP = asyncio.new_event_loop()
# New asyncio event loop for handling asynchronous operations

START_TIME = time.time()
# Timestamp for tracking the start time of operations


create_directory(LOG_FOLDER)


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