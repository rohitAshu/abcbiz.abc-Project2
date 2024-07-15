from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QWidget,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QHBoxLayout,
    QTextEdit,
)
import sys
import asyncio

from screeninfo import get_monitors
import scapping  # Make sure scrapping is imported correctly
from utils import (
    convent_into_csv_and_save,
    csv_to_json,
    print_the_output_statement,
    check_json_length,
)
import time
from datetime import datetime
import json

# Constants for file naming and paths Save data
FILE_NAME = "abcbiz_report"
REPORT_FOLDER = "Daily_Report"
FILE_TYPE = "csv"
CURRENT_DATE = datetime.now()

LOGINURL = "https://abcbiz.abc.ca.gov/login"  # URL for licensing reports
# Headless
HEADLESS = True  # Whether to run the app in headless mode (no GUI)
FILE_NAME = "ABCGovtWebscrapping"


class LoginFormApp(QMainWindow):
    """A class representing the login form application.

    This application allows users to log in, upload CSV files, and scrape data.

    Attributes:
        page (obj): The current page object.
        browser (obj): The current browser object.
        start_time (float): The start time of the application.
        file_path (str): The file path of the selected CSV file.
    """

    def __init__(self):
        """
        Initialize the LoginFormApp class and set up the UI components.

        This method sets up the main window properties, form layout, and various widgets
        such as input fields, buttons, and an output area for displaying scraping results.
        """
        super().__init__()

        # Set the window properties (title and initial size)
        self.page = None
        self.browser = None
        self.start_time = time.time()
        self.setWindowTitle("Login Form")
        self.setGeometry(
            100, 100, 400, 300
        )  # Adjusted height to accommodate output area

        # Create central widget for the main window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create your form layout and widgets here
        layout = QFormLayout()
        self.username_field = QLineEdit()
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(
            QLineEdit.Password
        )  # Set password field to hide input
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close_window)
        layout.addRow(QLabel("Username:"), self.username_field)
        layout.addRow(QLabel("Password:"), self.password_field)
        layout.addRow(self.login_button, self.close_button)

        # Initialize button layout for Upload CSV and Scrap Data buttons
        self.button_layout = QHBoxLayout()
        self.upload_csv_button = QPushButton("Upload CSV")
        self.upload_csv_button.setEnabled(False)  # Initially disabled
        self.upload_csv_button.clicked.connect(self.upload_csv)
        self.scrap_data_button = QPushButton("Scrap Data")
        self.scrap_data_button.setEnabled(False)  # Initially disabled
        self.scrap_data_button.clicked.connect(self.scrap_data_button_clicked)
        self.button_layout.addWidget(self.upload_csv_button)
        self.button_layout.addWidget(self.scrap_data_button)
        layout.addRow(self.button_layout)

        # Output text area for scraping results
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)  # Make it read-only
        layout.addRow(QLabel("Output:"), self.output_text)

        central_widget.setLayout(layout)

        # Instance variable to store file_path
        self.file_path = ""

    def login(self):
        """
        Handle the login process for the user.

        This method retrieves the username and password from the input fields,
        validates the input, and performs an asynchronous login operation.
        If the login is successful, it updates the UI components accordingly.
        If the login fails, it displays an error message.

        Raises:
            ValidationError: If the username or password fields are empty.
            LoginError: If the login details are invalid.
        """
        username = self.username_field.text()
        password = self.password_field.text()
        # Validate input fields
        if username == "" or password == "":
            QMessageBox.warning(
                self, "Validation Error", "Please Enter the Username and Password"
            )
        else:
            # Perform asynchronous login operation
            (
                status,
                login_status,
                browser,
                page,
            ) = asyncio.get_event_loop().run_until_complete(
                scapping.abiotic_login(
                    username=username,
                    password=password,
                    output_text=self.output_text,
                    loginurl=LOGINURL,
                    headless=HEADLESS,
                    width=get_monitors()[0].width,
                    height=get_monitors()[0].height,
                )
            )
            print("login_status", login_status)
            self.browser = browser  # Store browser in instance variable
            self.page = page  # Store page in instance variable
            if status:
                # Update UI components on successful login
                self.username_field.setReadOnly(True)
                self.password_field.setReadOnly(True)
                self.login_button.clicked.disconnect()  # Disconnect the clicked signal
                self.upload_csv_button.setEnabled(True)
                self.scrap_data_button.setEnabled(False)
            else:
                # Display error message on login failure
                QMessageBox.warning(self, "Validation Error", "Invalid Login Details")
                print("Invalid Login Details")

    def scrap_data(self, file_path):
        """Placeholder function for scraping data.

        Args:
            file_path (str): The file path of the selected CSV file.
        """
        print("Scraping data...")
        print(file_path)
        # Add your scraping or processing logic here
        # Example: Display file path in output_text
        self.output_text.append(f"Scraping data from: {file_path}")

    def upload_csv(self):
        """
        Handle the CSV file upload process, including validation and updating UI components.

        This method opens a file dialog to allow the user to select a CSV file. If a file is selected,
        it stores the file path in an instance variable and enables the "Scrap Data" button.
        If no file is selected, it displays an error message.

        Raises:
            ValidationError: If no file is selected or if the selected file is not a CSV file.
        """
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select File Name", "", "CSV Files (*.csv)", options=options
        )
        if file_path:
            self.file_path = file_path  # Store file_path in instance variable
            self.scrap_data_button.setEnabled(True)  # Enable Scrap Data button
        else:
            # Display an error message if no file is selected
            QMessageBox.warning(
                self, "Validation Error", "Please Choose the Correct CSV FILE"
            )

    def scrap_data_button_clicked(self):
        """
        Handle button click event for scraping data from a selected CSV file.

        This method performs the following steps:
        1. Retrieve the file path, browser, and page from the class attributes.
        2. Check if a CSV file path is selected.
        3. Converts the selected CSV file to JSON format and retrieves the headers.
        4. Validates the JSON data and checks for missing headers ('service_number' and 'last_name').
        5. Loads the JSON data into a Python object and performs data scraping asynchronously.
        6. Saves the scraped data to a CSV file and logs the output file path.
        7. Handles errors gracefully and displays appropriate error messages.
        8. Calculates and logs the total execution time of the method.

        Returns:
            None

        Raises:
            QMessageBox.warning: If no CSV file path is selected.
        """
        file_path = self.file_path  # Get the file path from class attributes
        browser = self.browser  # Get the browser instance from class attributes
        page = self.page  # Get the page instance from class attributes

        if file_path:
            # Print a message indicating the CSV file selected
            print_the_output_statement(self.output_text, f"CSV file selected {file_path}")

            # Convert CSV to JSON
            csv_header, json_data_str = csv_to_json(file_path)

            # Check the length of the JSON data
            json_length = check_json_length(json_data_str)
            if json_length != -1:
                print("json_length", json_length)

                # Check for missing headers in the CSV compared to expected headers
                missing_headers = [
                    header for header in ["service_number", "last_name"] if header not in csv_header
                ]
                if missing_headers:
                    print("if missing_headers:")
                    # Log and display missing headers in the output text
                    print_the_output_statement(self.output_text, f"Missing headers in CSV: {missing_headers}")
                else:
                    print("else missing_headers:")
                    # Load JSON data into a Python object
                    json_object = json.loads(json_data_str)
                    if json_object:
                        print("if json_object:")
                        # Perform scraping using asyncio
                        status, scrapping_status = asyncio.get_event_loop().run_until_complete(
                            scraping.scrapping_data(
                                browser=browser,
                                page=page,
                                resource=json_object,
                                output_text=self.output_text,
                            )
                        )
                        if status:
                            print("if status:")
                            # Define an output file path for saving scraped data
                            outputfile = f"{REPORT_FOLDER}/{CURRENT_DATE.strftime('%Y-%m-%d')}/{FILE_NAME}_generate_report_{CURRENT_DATE.strftime('%Y-%B-%d')}.{FILE_TYPE}"
                            print("outputfile", outputfile)

                            # Save scraped data to CSV
                            convert_into_csv_and_save(scrapping_status, outputfile)
                            # Log and display a success message
                            print_the_output_statement(self.output_text, f"data saved successfully to {outputfile}")
                        else:
                            print("Something Wrong")
                    else:
                        print("else json_object:")
                        # Log and display a message if JSON object is empty
                        print_the_output_statement(self.output_text, "JSON is empty")
            else:
                # Log and display message if JSON data is invalid
                print_the_output_statement(self.output_text, "Invalid JSON file")
        else:
            # Show a warning dialog if no file path is selected
            QMessageBox.warning(self, "Validation Error", "Invalid CSV file")

        # Calculate and log total execution time
        total_time = time.time() - self.start_time
        print_the_output_statement(self.output_text, f"Total execution time: {total_time:.2f} seconds")



    def close_window(self):
        """Close the application window."""
        self.close()


def main():
    """Main function to run the application."""
    app = QApplication(sys.argv)
    window = LoginFormApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
