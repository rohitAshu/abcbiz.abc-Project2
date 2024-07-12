from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QFormLayout, QLabel, QLineEdit, \
    QPushButton, QMessageBox, QHBoxLayout, QTextEdit
import sys
import asyncio
import scapping  # Make sure scrapping is imported correctly
from utils import csv_to_json, print_the_output_statement
import time


class LoginFormApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window properties (title and initial size)
        self.page = None
        self.browser = None
        self.start_time = time.time()
        self.setWindowTitle("Login Form")
        self.setGeometry(100, 100, 400, 300)  # Adjusted height to accommodate output area

        # Create central widget for the main window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create your form layout and widgets here
        layout = QFormLayout()
        self.username_field = QLineEdit()
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)
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
        self.file_path = ''

    def login(self):
        username = self.username_field.text()
        password = self.password_field.text()

        if username == "" or password == "":
            QMessageBox.warning(self, "Validation Error", "Please Enter the Username and Password")
        else:
            status, login_status, browser, page = asyncio.get_event_loop().run_until_complete(
                scapping.abiotic_login(username=username, password=password, output_text=self.output_text))
            print('login_status', login_status)
            self.browser = browser  # Store file_path in instance variable
            self.page = page  # Store file_path in instance variable
            if status:
                self.username_field.setReadOnly(True)
                self.password_field.setReadOnly(True)
                self.login_button.clicked.disconnect()  # Disconnect the clicked signal
                self.upload_csv_button.setEnabled(True)
                self.scrap_data_button.setEnabled(False)
            else:
                QMessageBox.warning(self, "Validation Error", "Invalid Login Details")
                print('Invalid Login Details')

    def scrap_data(self, file_path):
        print('Scraping data...')
        print(file_path)
        # Add your scraping or processing logic here
        # Example: Display file path in output_text
        self.output_text.append(f"Scraping data from: {file_path}")

    def upload_csv(self):

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File Name", "", "CSV Files (*.csv)", options=options)
        if file_path:
            self.file_path = file_path  # Store file_path in instance variable
            # self.print_the_output_statement(output_text, 'CSV file selected')
            self.scrap_data_button.setEnabled(True)
        else:
            QMessageBox.warning(self, "Validation Error", "Please Choose the Correct CSV FILE")

    def scrap_data_button_clicked(self):
        file_path = self.file_path
        browser = self.browser
        page = self.page
        if file_path:
            print_the_output_statement(self.output_text, f'CSV file selected {file_path}')
            resource = csv_to_json(file_path)
            status, scrapping_status, = asyncio.get_event_loop().run_until_complete(
                scapping.scrapping_data(browser=browser, page=page, resource=resource, output_text=self.output_text))
            print(scrapping_status)
        else:
            QMessageBox.warning(self, "Validation Error", "Invalid Csv file")
        total_time = time.time() - self.start_time
        print_the_output_statement(
            self.output_text, f"Total execution time: {total_time:.2f} seconds"
        )

    def close_window(self):
        self.close()


def main():
    app = QApplication(sys.argv)
    window = LoginFormApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
