import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, QObject
from PyQt5.QtGui import QFont
from config import APP_NAME, APP_TITLE
from utils import center_window, print_the_output_statement
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
    background-color: rgba(0, 123, 255, 0.1); /* Simulating box-shadow effect */
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
class MainWindow(QMainWindow):
    """
    MainWindow class for the PyQt application. It handles user interactions, including login, file upload,
    data scraping, and output display.

    Attributes:
        username_field (QLineEdit): Input field for the username.
        password_field (QLineEdit): Input field for the password.
        login_button (QPushButton): Button to initiate login.
        close_button (QPushButton): Button to close the browser.
        upload_csv_button (QPushButton): Button to upload an Excel file.
        scrap_data_button (QPushButton): Button to start data scraping.
        output_text (QTextEdit): Widget to display output and status messages.
    """

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(APP_TITLE)
        self.setGeometry(500, 600, 1000, 500)
        center_window(self)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        app_title_label = QLabel(f"<h1>{APP_NAME}</h1>")
        app_title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(app_title_label)
        # IMplementation the Fonts
        font = QFont()
        font.setBold(True)
        # Form Layout
        form_layout = QVBoxLayout()
        form_layout.addSpacing(20)
        layout.addLayout(form_layout)
        # added teh Form layout for  username
        form_layout.addWidget(QLabel("<b>Enter the username and email address:</b>"))
        self.username_field = QLineEdit()
        self.username_field.setPlaceholderText("Enter the username and email address")
        self.username_field.setFont(font)
        self.username_field.setStyleSheet("height: 20px;")
        form_layout.addWidget(self.username_field)
        # added teh Form layout for  password
        form_layout.addWidget(QLabel("<b>Enter the password:</b>"))
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setStyleSheet("height: 20px;")
        self.password_field.setPlaceholderText("Enter the password")
        self.password_field.setFont(font)
        form_layout.addWidget(self.password_field)

        button_layout = QHBoxLayout()
        form_layout.addLayout(button_layout)
        # added Button Layout for Login
        self.login_button = QPushButton("Login")
        self.login_button.setFont(font)
        self.login_button.clicked.connect(self.login_function)
        button_layout.addWidget(self.login_button)

        self.close_button = QPushButton("Close Window")
        self.close_button.clicked.connect(self.closed_window)

        self.close_button.setFont(font)
        button_layout.addWidget(self.close_button)

        bottom_button_layout = QHBoxLayout()
        layout.addLayout(bottom_button_layout)

        self.upload_csv_button = QPushButton("Upload Excel File")
        self.upload_csv_button.setEnabled(False)
        self.upload_csv_button.clicked.connect(self.upload_excel)
        self.upload_csv_button.setFont(font)
        bottom_button_layout.addWidget(self.upload_csv_button)

        self.scrap_data_button = QPushButton("Scrap Data")
        self.scrap_data_button.setEnabled(False)
        self.scrap_data_button.clicked.connect(self.scrap_data_button_clicked)
        self.scrap_data_button.setFont(font)
        bottom_button_layout.addWidget(self.scrap_data_button)

        layout.addWidget(QLabel("<b>Output:</b>"))
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Arial", 12))
        layout.addWidget(self.output_text)

    def login_function(self):
        print_the_output_statement(self.output_text, ' def login_function(self):')

    def upload_excel(self):
        print_the_output_statement(self.output_text, 'def upload_excel(self):')

    def scrap_data_button_clicked(self):
        print_the_output_statement(self.output_text, 'def scrap_data_button_clicked(self):')
       
    def closed_window(self):
       print_the_output_statement(self.output_text, 'def closed_window(self):')

if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    app.setStyleSheet(bootstrap_style)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())