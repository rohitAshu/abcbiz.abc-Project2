"""
This script initializes and runs a PyQt-based GUI application for web scraping and data handling.

Modules:
    - config: Configuration settings for the application.
    - scrapping: Module for web scraping functionalities.
    - time: Provides time-related functions.
    - json: Provides methods for parsing and creating JSON data.
    - sys: Provides access to system-specific parameters and functions.
    - asyncio: Provides support for asynchronous programming.
    - PyQt5.QtWidgets: Provides GUI elements for the application.
    - PyQt5.QtCore: Provides core non-GUI functionality for PyQt applications.
    - utils: Utility functions for various tasks, including window centering, JSON handling, CSV conversion, stylesheet loading, output printing, and message box display.
"""

from config import *
import scrapping  # Ensure scrapping is imported correctly
import time
import sys
import asyncio
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QHBoxLayout,
    QTextEdit,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils import (
    center_window,
    convert_into_csv_and_save,
    load_stylesheet,
    print_the_output_statement,
    show_message_box,
    xlsx_to_json,
)


class LoginFormApp(QMainWindow):
    def __init__(self):
        """
        Initializes the main window, sets the window title and geometry,
        centers the window on the screen, initializes the start time,
        and sets up the UI.
        """
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setGeometry(500, 600, 1000, 500)
        center_window(self)
        self.start_time = time.time()  # Initialize start_time
        self.initUI()

    def initUI(self):
        """
        Sets up the user interface of the main window.

        This method creates labels, input fields for username and password,
        login and close buttons, upload CSV and scrap data buttons, and an output text area.

        Signals are connected for login, close, upload CSV, and scrap data buttons.
        """
        print("initUI call")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create vertical layout for central widget
        layout = QVBoxLayout()
        # Application title label
        app_title_label = QLabel(f"<h1> {APP_NAME}</h1>")
        app_title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(app_title_label)

        central_widget.setLayout(layout)

        font = QFont()
        font.setBold(True)

        # Form layout for username and password
        form_layout = QVBoxLayout()
        form_layout.addSpacing(20)
        layout.addLayout(form_layout)

        # Username Label
        form_layout.addWidget(QLabel("<b>Enter the username and email address:</b>"))
        # Username Input Field
        self.username_field = QLineEdit()
        self.username_field.setPlaceholderText("Enter the username and email address")
        self.username_field.setFont(font)
        self.username_field.setStyleSheet("height: 20px;")  # Example: increase height
        form_layout.addWidget(self.username_field)

        # Password Label
        form_layout.addWidget(QLabel("<b>Enter the password:</b>"))
        # Password Input Field
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setStyleSheet("height: 20px;")  # Example: increase height
        self.password_field.setPlaceholderText("Enter the password")
        self.password_field.setFont(font)
        form_layout.addWidget(self.password_field)

        # Button layout for login and close buttons
        button_layout = QHBoxLayout()
        form_layout.addLayout(button_layout)

        # Login Button Layout
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        self.login_button.setFont(font)
        button_layout.addWidget(self.login_button)

        # Close Button Layout
        self.close_button = QPushButton("Close Browser")
        self.close_button.clicked.connect(self.close_window)
        self.close_button.setFont(font)
        button_layout.addWidget(self.close_button)

        # Separate button layout for upload CSV and scrap data buttons
        bottom_button_layout = QHBoxLayout()
        layout.addLayout(bottom_button_layout)

        # Upload CSV Button Style and Design
        self.upload_csv_button = QPushButton("Upload CSV")
        self.upload_csv_button.setEnabled(False)
        self.upload_csv_button.clicked.connect(self.upload_csv)
        self.upload_csv_button.setFont(font)
        bottom_button_layout.addWidget(self.upload_csv_button)

        # Scrap Data Button Style and Design
        self.scrap_data_button = QPushButton("Scrap Data")
        self.scrap_data_button.setEnabled(False)
        self.scrap_data_button.clicked.connect(self.scrap_data_button_clicked)
        self.scrap_data_button.setFont(font)
        bottom_button_layout.addWidget(self.scrap_data_button)

        # Output text
        layout.addWidget(QLabel("<b>Output:</b>"))
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Arial", 12))  # Example: set font
        self.output_text.setFont(font)
        self.output_text.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        layout.addWidget(self.output_text)

        # Center the main window
        center_window(self)

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
            show_message_box(
                self,
                QMessageBox.Warning,
                "vaidation error",
                "Please Enter the Username and Password",
            )
        else:
            # Perform asynchronous login operation
            (
                status,
                login_status,
                browser,
                page,
            ) = asyncio.get_event_loop().run_until_complete(
                scrapping.abiotic_login(
                    username=username, password=password, output_text=self.output_text
                )
            )
            self.browser = browser  # Store browser in instance variable
            self.page = page  # Store page in instance variable
            if status:
                print("login_status", login_status)
                print_the_output_statement( self.output_text, login_status)
                # Update UI components on successful login
                self.username_field.setReadOnly(True)
                self.password_field.setReadOnly(True)
                self.upload_csv_button.setEnabled(True)
                self.scrap_data_button.setEnabled(False)
                self.login_button.setEnabled(False)
            else:
                show_message_box(
                    self,
                    QMessageBox.Warning,
                    "vaidation error",
                    "Invalid Login Details and please enter login Details",
                )
                print("Invalid Login Details")

    def scrap_data(self, file_path):
        print("Scraping data...")
        print(file_path)
        self.output_text.append(f"Scraping data from: {file_path}")

    def upload_csv(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
        self, "Select File Name", "", "Excel Files (*.xlsx)", options=options
    )
        if file_path:
            self.file_path = file_path  # Store file_path in instance variable
            self.scrap_data_button.setEnabled(True)  # Enable Scrap Data button
            self.upload_csv_button.setEnabled(False)  # Enable Scrap Data button
            print_the_output_statement(
                self.output_text, f"excel  file selected {file_path}"
            )
        else:
            self.scrap_data_button.setEnabled(False)  # Enable Scrap Data button
            self.upload_csv_button.setEnabled(True)  # Enable Scrap Data button
            show_message_box(
                self,
                QMessageBox.Warning,
                "File Error",
                "Please Choose the Correct CSV FILE",
            )

    def scrap_data_button_clicked(self):
        file_path = self.file_path  # Get the file path from class attributes
        browser = self.browser  # Get the browser instance from class attributes
        page = self.page  # Get the page instance from class attributes
        print_the_output_statement(
            self.output_text, "Scrapping started, please wait for few minutes."
        )
        if file_path:
            csv_header, json_data_str, num_records = xlsx_to_json(file_path)
            if num_records > 0:
                print("json data is found")
                missing_headers = [ header for header in ["Server_ID", "Last_Name"] if header not in csv_header]
                if missing_headers:
                    print("if missing_headers:")
                    self.upload_csv_button.setEnabled(True)
                    self.scrap_data_button.setEnabled(False)
                    show_message_box(self, QMessageBox.Warning,"File Error", "missing the header in the csv please choose the correct excel ",)
                else:
                    print('Hellooooooooooo ')
                    status, scrapping_status = asyncio.get_event_loop().run_until_complete(
                            scrapping.scrapping_data(
                                browser, page, json_data_str , self.output_text
)
                        )
                    if status:
                        print_the_output_statement(
                                self.output_text, f"Scraping completed."
                            )
                        options = QFileDialog.Options()
                        folder_path = QFileDialog.getExistingDirectory( self, "Select Directory", options=options)
                        if folder_path:
                            outputfile = f"{folder_path}/{FILE_NAME}_generate_report_{CURRENT_DATE.strftime('%Y-%B-%d')}.{FILE_TYPE}"
                            print("outputfile", outputfile)
                            convert_into_csv_and_save(scrapping_status, outputfile)
                            self.login_button.setEnabled(True)
                            self.scrap_data_button.setEnabled(False)
                            self.upload_csv_button.setEnabled(False)
                            print_the_output_statement(
                                    self.output_text,
                                    f"Data saved successfully to {outputfile}",
                                )
                            show_message_box(
                                    self,
                                    QMessageBox.NoIcon,
                                    "success",
                                    f"Data saved successfully to {outputfile}",
                                )
                        else:
                            show_message_box( self, QMessageBox.Warning,"error", "data successfully found succssfully but failed to the saved the data" )
                    else:
                        print('Something Wrong')
            else:
                self.upload_csv_button.setEnabled(True)
                self.scrap_data_button.setEnabled(False)
                print("json data is not Found")
                self.upload_csv_button.setEnabled(True)
                self.scrap_data_button.setEnabled(False)
                show_message_box(self, QMessageBox.Warning,"File Error", "excel is empty please choose another execel sheet",)
    
    def close_window(self):
        """
        Prompt the user with a confirmation message box to close the window.

        If the user clicks 'Yes' in the confirmation message box, the window is closed.

        Returns:
            None
        """
        result = show_message_box(
            self,
            QMessageBox.Question,
            "Confirmation",
            "Are you sure you want to close the browser?",
        )
        if result == QMessageBox.Yes:
            self.close()  # Close the window if user clicks 'Yes'


def main():
    """
    Main function to run the application.

    Initializes the QApplication, sets the stylesheet, creates and shows the login form window,
    and starts the application event loop.

    Usage:
        - Ensure 'css/style.css' exists for the stylesheet to be loaded correctly.
        - Replace 'LoginFormApp' with your actual login form application class.

    Returns:
        None
    """
    app = QApplication(sys.argv)  # Create the QApplication instance

    css_file_path = os.path.join("css", "style.css")  # Path to your stylesheet
    app.setStyleSheet(load_stylesheet(css_file_path))  # Load and apply the stylesheet

    window = LoginFormApp()  # Create an instance of your login form application
    window.show()  # Show the login form window

    sys.exit(app.exec_())  # Start the application event loop and exit when it's done


if __name__ == "__main__":
    main()
