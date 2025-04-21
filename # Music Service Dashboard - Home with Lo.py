# Music Service App - Full Home, Login, Sign Up, Genre Selection

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QStackedWidget, QLineEdit, QMessageBox, QDateEdit, QComboBox, QCheckBox
)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, QDate
from sqlalchemy import create_engine

# DB Setup
engine = create_engine(
    'mssql+pyodbc://@LAPTOP-F7KBVO5O\\SQLEXPRESS01/CSS665_PROIJECT?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
)
conn = engine.raw_connection()
cursor = conn.cursor()

class MusicApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎶 Music Vibe")
        self.setGeometry(100, 100, 1100, 700)
        self.set_light_green_theme()
        self.current_user_id = None
        self.stack = QStackedWidget()
        self.init_ui()

    def set_light_green_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(200, 255, 200))  # Light green
        palette.setColor(QPalette.WindowText, Qt.black)
        palette.setColor(QPalette.Base, QColor(240, 255, 240))
        palette.setColor(QPalette.Text, Qt.black)
        palette.setColor(QPalette.Button, QColor(144, 238, 144))
        palette.setColor(QPalette.ButtonText, Qt.black)
        self.setPalette(palette)

    def init_ui(self):
        self.stack.addWidget(self.create_home_page())       # 0
        self.stack.addWidget(self.create_login_page())      # 1
        self.stack.addWidget(self.create_signup_page())     # 2
        self.stack.addWidget(self.create_genre_page())      # 3

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)

    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("🎧 WELCOME TO MUSIC VIBE")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: green; margin: 20px;")

        login_btn = QPushButton("🔐 Login")
        signup_btn = QPushButton("✍️ Sign Up")
        for btn in [login_btn, signup_btn]:
            btn.setStyleSheet("padding: 12px; font-size: 16px; font-weight: bold; margin: 10px; background-color: #4CAF50; color: white; border-radius: 8px;")

        login_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        signup_btn.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        layout.addWidget(title)
        layout.addWidget(login_btn, alignment=Qt.AlignCenter)
        layout.addWidget(signup_btn, alignment=Qt.AlignCenter)
        page.setLayout(layout)
        return page

    def create_login_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("🔐 Login to Your Account")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: green;")

        self.login_email_input = QLineEdit()
        self.login_email_input.setPlaceholderText("Email")
        self.login_email_input.setStyleSheet("padding: 8px;")

        login_btn = QPushButton("Login")
        login_btn.setStyleSheet("padding: 10px; font-weight: bold; background-color: #2196F3; color: white; border-radius: 6px;")
        login_btn.clicked.connect(self.handle_login)

        layout.addWidget(title)
        layout.addWidget(self.login_email_input)
        layout.addWidget(login_btn, alignment=Qt.AlignCenter)
        page.setLayout(layout)
        return page

    def create_signup_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("✍️ Create a New Account")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: green;")

        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.dob = QDateEdit()
        self.signup_email = QLineEdit()
        self.first_name.setPlaceholderText("First Name")
        self.last_name.setPlaceholderText("Last Name")
        self.signup_email.setPlaceholderText("Email")
        self.dob.setCalendarPopup(True)
        self.dob.setDate(QDate.currentDate())

        for w in [self.first_name, self.last_name, self.dob, self.signup_email]:
            w.setStyleSheet("padding: 8px; background-color: white; color: black; margin: 5px;")

        signup_btn = QPushButton("Sign Up")
        signup_btn.setStyleSheet("padding: 10px; font-weight: bold; background-color: #4CAF50; color: white; border-radius: 6px;")
        signup_btn.clicked.connect(self.handle_signup)

        layout.addWidget(title)
        layout.addWidget(self.first_name)
        layout.addWidget(self.last_name)
        layout.addWidget(self.dob)
        layout.addWidget(self.signup_email)
        layout.addWidget(signup_btn, alignment=Qt.AlignCenter)
        page.setLayout(layout)
        return page

    def create_genre_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("🎵 Select Your Favorite Music Genres")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 20px; font-weight: bold; color: green;")

        genres = ["Pop music", "Hip-hop", "Electronic music", "Rhythm and blues",
                  "Popular music", "Heavy metal", "Folk music", "Country music", "Jazz"]

        self.genre_checks = []
        for genre in genres:
            chk = QCheckBox(genre)
            chk.setStyleSheet("color: black; font-size: 16px;")
            self.genre_checks.append(chk)
            layout.addWidget(chk)

        submit = QPushButton("Save Preferences")
        submit.setStyleSheet("padding: 10px; font-weight: bold; background-color: #2196F3; color: white; border-radius: 6px;")
        submit.clicked.connect(self.save_genres)

        layout.addWidget(label)
        layout.addWidget(submit, alignment=Qt.AlignCenter)
        page.setLayout(layout)
        return page

    def handle_login(self):
        email = self.login_email_input.text()
        cursor.execute("SELECT user_id FROM Users WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row:
            self.current_user_id = row[0]
            self.stack.setCurrentIndex(3)
        else:
            QMessageBox.warning(self, "Login Failed", "No account found. Please Sign Up.")
            self.stack.setCurrentIndex(2)

    def handle_signup(self):
        fname = self.first_name.text()
        lname = self.last_name.text()
        dob = self.dob.date().toString("yyyy-MM-dd")
        email = self.signup_email.text()
        try:
            cursor.execute("INSERT INTO Users (username, email, created_at) VALUES (?, ?, GETDATE())", (fname + " " + lname, email))
            conn.commit()
            cursor.execute("SELECT SCOPE_IDENTITY()")
            self.current_user_id = int(cursor.fetchone()[0])
            self.stack.setCurrentIndex(3)
        except Exception as e:
            QMessageBox.critical(self, "Signup Error", str(e))

    def save_genres(self):
        selected = [chk.text() for chk in self.genre_checks if chk.isChecked()]
        QMessageBox.information(self, "Preferences Saved", f"You selected: {', '.join(selected)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MusicApp()
    win.show()
    sys.exit(app.exec_())