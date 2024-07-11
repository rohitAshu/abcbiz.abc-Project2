import json
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFormLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import asyncio
import ascd

class LoginFormApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window properties (title and initial size)
        self.setWindowTitle("Login Form")
        self.setGeometry(100, 100, 400, 200)  # (x, y, width, height)

        # Create a central widget for the main window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a QFormLayout to arrange the widgets
        form_layout = QFormLayout()

        # Create QLabel and QLineEdit widgets for username
        username_label = QLabel("Username:")
        self.username_field = QLineEdit()

        # Create QLabel and QLineEdit widgets for password
        password_label = QLabel("Password:")
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)

        # Create a QPushButton for login
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)

        # Add widgets to the form layout
        form_layout.addRow(username_label, self.username_field)
        form_layout.addRow(password_label, self.password_field)
        form_layout.addRow(login_button, close_button)

        # Set the layout for the central widget
        central_widget.setLayout(form_layout)

    def closewindoes(self):
        self.close()

    def login(self):
        # Retrieve the username and password entered by the user
        username = self.username_field.text()
        password = self.password_field.text()

        if username == "" or password == "":
            QMessageBox.warning(self, "Validation Error", "Please Enter the Username and password")
        else:
            json_data = '''
                {
                    "service_number": "313018426",
                    "last_name": "Angeles"
                }
                '''
            data = json.loads(json_data)
            service_number = data.get('service_number')
            last_name = data.get('last_name')
            print('service_number', service_number)
            print('last_name', last_name)
            asyncio.get_event_loop().run_until_complete(
                ascd.main(service_number=service_number, last_name=last_name, username=username, password=password))

def main():
    app = QApplication(sys.argv)
    window = LoginFormApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
