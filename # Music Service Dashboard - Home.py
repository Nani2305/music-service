# Music Service Dashboard - Home with Login + Playlist Control + User Session Management

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QStackedWidget, QTableWidget, QTableWidgetItem, QLineEdit, QHeaderView,
    QMessageBox, QFrame, QComboBox
)
from PyQt5.QtGui import QPixmap, QPalette, QColor
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
        self.setWindowTitle("🎶 Music Vibe")
        self.setGeometry(100, 100, 1200, 700)
        self.current_user_id = None
        self.set_dark_mode()
        self.init_ui()

    def set_dark_mode(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(34, 34, 34))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(60, 60, 60))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.Highlight, QColor(0, 150, 0))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.stack = QStackedWidget()

        self.stack.addWidget(self.create_home_page())
        self.stack.addWidget(self.create_login_signup_page())
        self.stack.addWidget(self.create_library_page())

        self.layout.addWidget(self.stack)
        self.setLayout(self.layout)

    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("🎧 WELCOME TO MUSIC VIBE")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: white; margin-top: 40px;")

        bg_image = QLabel()
        pix = QPixmap(1000, 300)
        pix.fill(QColor("#228B22"))
        bg_image.setPixmap(pix)
        bg_image.setAlignment(Qt.AlignCenter)
        bg_image.setStyleSheet("border-radius: 10px; margin: 10px auto;")

        cta = QPushButton("🚀 Login or Sign Up to Start")
        cta.setStyleSheet("padding: 14px; font-size: 16px; font-weight: bold; background-color: #4CAF50; color: white; border-radius: 10px;")
        cta.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        layout.addWidget(title)
        layout.addWidget(bg_image)
        layout.addWidget(cta, alignment=Qt.AlignCenter)
        page.setLayout(layout)
        return page

    def create_login_signup_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("👤 Create Account or Login")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        for widget in [self.username_input, self.email_input]:
            widget.setStyleSheet("padding: 8px; background-color: white; color: black; border-radius: 5px;")

        submit_btn = QPushButton("✅ Enter Library")
        submit_btn.setStyleSheet("padding: 10px; background-color: #2196F3; color: white; font-weight: bold; border-radius: 8px;")
        submit_btn.clicked.connect(self.handle_login)

        layout.addWidget(label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.email_input)
        layout.addWidget(submit_btn, alignment=Qt.AlignCenter)
        page.setLayout(layout)
        return page

    def handle_login(self):
        username = self.username_input.text()
        email = self.email_input.text()
        cursor.execute("SELECT user_id FROM Users WHERE username = ? AND email = ?", (username, email))
        result = cursor.fetchone()
        if result:
            self.current_user_id = result[0]
        else:
            cursor.execute("INSERT INTO Users (username, email, created_at) VALUES (?, ?, GETDATE())", (username, email))
            conn.commit()
            cursor.execute("SELECT SCOPE_IDENTITY()")
            self.current_user_id = int(cursor.fetchone()[0])
        self.load_songs()
        self.stack.setCurrentIndex(2)

    def create_library_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("🎵 Library - Manage Your Songs and Playlist")
        label.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        layout.addWidget(label)

        self.song_table = QTableWidget()
        self.song_table.setColumnCount(5)
        self.song_table.setHorizontalHeaderLabels(["Song ID", "Title", "Artist ID", "Duration", "Release Year"])
        self.song_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.song_table.setStyleSheet("QHeaderView::section { background-color: #666; color: white; font-weight: bold; } QTableWidget { background-color: #2e2e2e; color: white; }")
        layout.addWidget(self.song_table)

        playlist_label = QLabel("Select Playlist to Add Song:")
        playlist_label.setStyleSheet("color: white;")
        self.playlist_combo = QComboBox()
        self.playlist_combo.setStyleSheet("background-color: white; color: black;")
        layout.addWidget(playlist_label)
        layout.addWidget(self.playlist_combo)

        add_btn = QPushButton("➕ Add to Playlist")
        add_btn.setStyleSheet("padding: 8px; background-color: #4CAF50; color: white; font-weight: bold; border-radius: 6px;")
        add_btn.clicked.connect(self.add_song_to_playlist)
        layout.addWidget(add_btn)

        refresh_btn = QPushButton("🔄 Refresh Songs")
        refresh_btn.setStyleSheet("padding: 8px; background-color: #0f9d58; color: white; font-weight: bold; border-radius: 6px;")
        refresh_btn.clicked.connect(self.load_songs)
        layout.addWidget(refresh_btn)

        page.setLayout(layout)
        return page

    def load_songs(self):
        self.song_table.setRowCount(0)
        self.playlist_combo.clear()
        try:
            cursor.execute("SELECT playlist_id, name FROM Playlists WHERE user_id = ?", (self.current_user_id,))
            for row in cursor.fetchall():
                self.playlist_combo.addItem(f"{row[1]} (ID: {row[0]})", row[0])

            cursor.execute("SELECT song_id, title, artist_id, duration, release_year FROM Songs")
            for i, row in enumerate(cursor.fetchall()):
                self.song_table.insertRow(i)
                for j, val in enumerate(row):
                    self.song_table.setItem(i, j, QTableWidgetItem(str(val)))
        except Exception as e:
            QMessageBox.critical(self, "DB Error", str(e))

    def add_song_to_playlist(self):
        row = self.song_table.currentRow()
        if row >= 0:
            song_id = self.song_table.item(row, 0).text()
            playlist_id = self.playlist_combo.currentData()
            try:
                cursor.execute("INSERT INTO Playlist_Songs (playlist_id, song_id) VALUES (?, ?)", (playlist_id, song_id))
                conn.commit()
                QMessageBox.information(self, "Success", "Song added to playlist!")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MusicApp()
    win.show()
    sys.exit(app.exec_())
