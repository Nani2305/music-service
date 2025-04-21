# Music Service Dashboard - Modern GUI with Home + Library + Accounts Tabs

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QStackedWidget, QTableWidget, QTableWidgetItem, QLineEdit, QHeaderView,
    QFrame, QMessageBox
)
from PyQt5.QtGui import QPixmap, QPalette, QColor, QFont
from PyQt5.QtCore import Qt
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
        self.setWindowTitle("🎶 Music Stream Manager")
        self.setGeometry(100, 100, 1200, 700)
        self.set_dark_mode()
        self.init_ui()

    def set_dark_mode(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(25, 25, 25))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(35, 35, 35))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(45, 45, 45))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.Highlight, QColor(38, 79, 120))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        self.setPalette(palette)

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Navbar
        nav = QHBoxLayout()
        self.btn_home = QPushButton("🏠 Home")
        self.btn_library = QPushButton("🎵 Library")
        self.btn_accounts = QPushButton("👤 Accounts")
        for btn in [self.btn_home, self.btn_library, self.btn_accounts]:
            btn.setStyleSheet("padding: 10px; background-color: #444; color: white; font-weight: bold; border-radius: 5px;")
        nav.addWidget(self.btn_home)
        nav.addWidget(self.btn_library)
        nav.addWidget(self.btn_accounts)

        # Stacked views
        self.stack = QStackedWidget()
        self.stack.addWidget(self.create_home_page())
        self.stack.addWidget(self.create_library_page())
        self.stack.addWidget(self.create_accounts_page())

        # Switch views
        self.btn_home.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_library.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_accounts.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        main_layout.addLayout(nav)
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        welcome = QLabel("🎧 Welcome to Your Music Service")
        welcome.setStyleSheet("font-size: 26px; font-weight: bold; color: white;")
        welcome.setAlignment(Qt.AlignCenter)

        banner = QLabel()
        pix = QPixmap(900, 250)
        pix.fill(QColor("#333"))
        banner.setPixmap(pix)
        banner.setAlignment(Qt.AlignCenter)
        banner.setStyleSheet("border: 2px solid #555;")
        banner_text = QLabel("Stream. Manage. Enjoy.")
        banner_text.setAlignment(Qt.AlignCenter)
        banner_text.setStyleSheet("font-size: 18px; color: white;")

        layout.addWidget(welcome)
        layout.addWidget(banner)
        layout.addWidget(banner_text)
        page.setLayout(layout)
        return page

    def create_library_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("📚 Library - Songs Table")
        label.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        layout.addWidget(label)

        self.songs_table = QTableWidget()
        self.songs_table.setColumnCount(5)
        self.songs_table.setHorizontalHeaderLabels(["ID", "Title", "Artist ID", "Duration", "Year"])
        self.songs_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.songs_table.setStyleSheet("QHeaderView::section { background-color: #666; color: white; font-weight: bold; } QTableWidget { background-color: #2e2e2e; color: white; }")
        layout.addWidget(self.songs_table)

        refresh_btn = QPushButton("🔁 Refresh Songs")
        refresh_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 10px; border-radius: 6px;")
        refresh_btn.clicked.connect(self.load_songs)
        layout.addWidget(refresh_btn)

        page.setLayout(layout)
        self.load_songs()
        return page

    def load_songs(self):
        self.songs_table.setRowCount(0)
        try:
            cursor.execute("SELECT song_id, title, artist_id, duration, release_year FROM Songs")
            for i, row in enumerate(cursor.fetchall()):
                self.songs_table.insertRow(i)
                for j, val in enumerate(row):
                    self.songs_table.setItem(i, j, QTableWidgetItem(str(val)))
        except Exception as e:
            QMessageBox.critical(self, "DB Error", str(e))

    def create_accounts_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        label = QLabel("👤 Accounts - Users Table")
        label.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        layout.addWidget(label)

        self.users_table = QTableWidget()
        self.users_table.setColumnCount(4)
        self.users_table.setHorizontalHeaderLabels(["ID", "Username", "Email", "Created At"])
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.users_table.setStyleSheet("QHeaderView::section { background-color: #666; color: white; font-weight: bold; } QTableWidget { background-color: #2e2e2e; color: white; }")
        layout.addWidget(self.users_table)

        refresh_btn = QPushButton("🔄 Refresh Users")
        refresh_btn.setStyleSheet("background-color: #673AB7; color: white; font-weight: bold; padding: 10px; border-radius: 6px;")
        refresh_btn.clicked.connect(self.load_users)
        layout.addWidget(refresh_btn)

        page.setLayout(layout)
        self.load_users()
        return page

    def load_users(self):
        self.users_table.setRowCount(0)
        try:
            cursor.execute("SELECT user_id, username, email, created_at FROM Users")
            for i, row in enumerate(cursor.fetchall()):
                self.users_table.insertRow(i)
                for j, val in enumerate(row):
                    self.users_table.setItem(i, j, QTableWidgetItem(str(val)))
        except Exception as e:
            QMessageBox.critical(self, "DB Error", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MusicApp()
    win.show()
    sys.exit(app.exec_())
