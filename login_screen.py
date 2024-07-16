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
    QDesktopWidget
    
)
import sys
import asyncio
from PyQt5.QtCore import Qt , QSize

from screeninfo import get_monitors
from config import *
import scapping  # Make sure scrapping is imported correctly
import time
from datetime import datetime
import json

from utils import check_json_length, convert_into_csv_and_save, csv_to_json, print_the_output_statement


bootstrap_style = """
QWidget {
    font-family: Arial, sans-serif;
    font-size: 14px;
}

QMainWindow {
    background-color: #f8f9fa;
}

QLabel {
    color: #212529;
}

QLineEdit {
    border: 1px solid #ced4da;
    border-radius: 4px;
    padding: 5px;
    font-size: 14px;
    color: #495057;
}

QLineEdit:focus {
    border-color: #80bdff;
    outline: 0;
    box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
}

QPushButton {
    background-color: #007bff;
    border: 1px solid #007bff;
    border-radius: 4px;
    color: white;
    padding: 5px 10px;
    font-size: 14px;
}

QPushButton:hover {
    background-color: #0056b3;
    border-color: #0056b3;
}

QPushButton:disabled {
    background-color: #6c757d;
    border-color: #6c757d;
    color: white;
}

QTextEdit {
    border: 1px solid #ced4da;
    border-radius: 4px;
    padding: 5px;
    font-size: 14px;
    color: #495057;
    background-color: white;
}
"""



class LoginFormApp(QMainWindow):
    """A class representing the login form application.

    This application allows users to log in, upload CSV files, and scrape data.

    Attributes:
        page (obj): The current page object.
        browser (obj): The current browser object.
        start_time (float): The start time of the application.
        file_path (str): The file path of the selected CSV file.
    """

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
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
            500, 500, 500, 500
        )  # Adjusted height to accommodate output area
        self.center()  # Center the window
        # Create central widget for the main window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Heading label for the form
        heading_label = QLabel("<h2>Login Form</h2>")
        heading_label.setAlignment(Qt.AlignCenter)


        # Application title label
        app_title_label = QLabel("<h1>ABCGovtWebscrapping</h1>")
        app_title_label.setAlignment(Qt.AlignCenter)

        # Create your form layout and widgets here
        layout = QFormLayout()
        layout.addRow(app_title_label)
        layout.addRow(heading_label)
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
                    output_text=self.output_text
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

        print("Scraping data...")
        print(file_path)
        # Add your scraping or processing logic here
        # Example: Display file path in output_text
        self.output_text.append(f"Scraping data from: {file_path}")

    def upload_csv(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select File Name", "", "CSV Files (*.csv)", options=options
        )
        if file_path:
            self.file_path = file_path  # Store file_path in instance variable
            self.scrap_data_button.setEnabled(True)  # Enable Scrap Data button
            self.upload_csv_button.setEnabled(False)  # Enable Scrap Data button
            print_the_output_statement(self.output_text, f"CSV file selected {file_path}")
        else:
            self.scrap_data_button.setEnabled(False)  # Enable Scrap Data button
            self.upload_csv_button.setEnabled(True)  # Enable Scrap Data button
            # Display an error message if no file is selected
            QMessageBox.warning(
                self, "Validation Error", "Please Choose the Correct CSV FILE"
            )

    def scrap_data_button_clicked(self):
        file_path = self.file_path  # Get the file path from class attributes
        browser = self.browser  # Get the browser instance from class attributes
        page = self.page  # Get the page instance from class attributes
        print_the_output_statement(self.output_text, "Scrapping started, please wait for few minutes.")
        if file_path:
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
                    print('missing the header in the csv')
                    self.upload_csv_button.setEnabled(True)
                    self.scrap_data_button.setEnabled(False)
                    QMessageBox.warning(self, "Validation Error", "missing the header in the csv")
                else:
                    print("else missing_headers:")
                    # Load JSON data into a Python object
                    json_object = json.loads(json_data_str)
                    if json_object:
                        print("if json_object:")
                        # Perform scraping using asyncio
                        status, scrapping_status = asyncio.get_event_loop().run_until_complete(
                            scapping.scrapping_data(
                                browser=browser,
                                page=page,
                                resource=json_object,
                                output_text=self.output_text,
                            )
                        )
                        if status:
                            print_the_output_statement(self.output_text, f"Scraping completed.")
                            self.upload_csv_button.setEnabled(False)
                            self.scrap_data_button.setEnabled(False)
                            self.login_button.setEnabled(True)
                            print("if status:")
                            print('scrapping_status',scrapping_status)
                            options = QFileDialog.Options()
                            folder_path = QFileDialog.getExistingDirectory(self, "Select Directory", options=options)
                            if folder_path:
                                outputfile = f"{folder_path}/{FILE_NAME}_generate_report_{CURRENT_DATE.strftime('%Y-%B-%d')}.{FILE_TYPE}"
                                print("outputfile", outputfile) 
                                convert_into_csv_and_save(scrapping_status, outputfile)
                                print_the_output_statement(self.output_text, f"Data saved successfully to {outputfile}")
                            else:
                                QMessageBox.warning(self, "Validation Error", "faild to the saved the data")
                                print('faild to the saved the data ')
                        else:
                            print("Something Wrong")
                            QMessageBox.warning(self, "Validation Error", "Something Wrong")
                            self.upload_csv_button.setEnabled(True)
                            self.scrap_data_button.setEnabled(False)
                    else:
                        QMessageBox.warning(self, "Validation Error", "CSV file is empty")
                        print('CSV file is empty')
                        self.upload_csv_button.setEnabled(True)
                        self.scrap_data_button.setEnabled(False)
            else:
                self.upload_csv_button.setEnabled(False)
                self.scrap_data_button.setEnabled(True)
                print('Invalid CSV file')
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
    app.setStyleSheet(bootstrap_style)
    window = LoginFormApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()