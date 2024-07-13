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
from utils import convet_into_csv_and_save, csv_to_json, print_the_output_statement
import time
from datetime import datetime

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
            # Display error message if no file is selected
            QMessageBox.warning(
                self, "Validation Error", "Please Choose the Correct CSV FILE"
            )

    def scrap_data_button_clicked(self):
        """
        Handle the data scraping process when the Scrap Data button is clicked.
        This method performs the following steps:
        1. Checks if a CSV file path is stored in the instance variable.
        2. Prints a message indicating the selected CSV file.
        3. Converts the CSV data to JSON format.
        4. Initiates the asynchronous data scraping process using the provided browser and page instances.
        5. If the scraping is successful, saves the scraped data to a CSV file and prints success messages.
        6. If the scraping fails, prints an error message.
        7. Displays the total execution time for the data scraping process.

        Raises:
            ValidationError: If the CSV file path is invalid.
        """
        file_path = self.file_path
        browser = self.browser
        page = self.page
        if file_path:
            print_the_output_statement(
                self.output_text, f"CSV file selected {file_path}"
            )
            resource = csv_to_json(file_path)  # Convert CSV to JSON
            (
                status,
                scrapping_status,
            ) = asyncio.get_event_loop().run_until_complete(
                scapping.scrapping_data(
                    browser=browser,
                    page=page,
                    resource=resource,
                    output_text=self.output_text,
                )
            )
            if status:
                # Define the output file path
                outputfile = f"{REPORT_FOLDER}/{CURRENT_DATE.strftime('%Y-%m-%d')}/{FILE_NAME}_generate_report_{CURRENT_DATE.strftime('%Y-%B-%d')}.{FILE_TYPE}"
                convet_into_csv_and_save(
                    scrapping_status, outputfile
                )  # Save scraped data to CSV
                print("data Scrapp Successfully")
                print_the_output_statement(
                    self.output_text, f"data save duccessfully save to {outputfile}"
                )
            else:
                print("Something Wrong")
        else:
            # Display error message if file path is invalid
            QMessageBox.warning(self, "Validation Error", "Invalid Csv file")
        total_time = time.time() - self.start_time
        print_the_output_statement(
            self.output_text, f"Total execution time: {total_time:.2f} seconds"
        )

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
