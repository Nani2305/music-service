import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QStackedWidget, QLineEdit, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from sqlalchemy import create_engine

# Database Setup
engine = create_engine(
    'mssql+pyodbc://@LAPTOP-F7KBVO5O\\SQLEXPRESS01/CSS665_PROIJECT?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
)
conn = engine.raw_connection()
cursor = conn.cursor()

class MusicApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎶 Music Vibe")
        self.setGeometry(100, 100, 1000, 600)
        self.set_light_theme()
        self.stack = QStackedWidget()
        self.init_ui()

    def set_light_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(245, 255, 245))
        palette.setColor(QPalette.WindowText, Qt.black)
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, Qt.black)
        palette.setColor(QPalette.Button, QColor(200, 255, 200))
        palette.setColor(QPalette.ButtonText, Qt.black)
        self.setPalette(palette)

    def init_ui(self):
        self.stack.addWidget(self.create_home_page())              # 0
        self.stack.addWidget(self.create_crud_page("Users_new", "Users", "user_id", ["username", "email"]))         # 1
        self.stack.addWidget(self.create_crud_page("Songs", "Songs", "song_id", ["title", "artist_id", "duration", "release_year"]))  # 2
        self.stack.addWidget(self.create_crud_page("Artists", "Artists", "artist_id", ["name", "genre", "country"]))  # 3
        self.stack.addWidget(self.create_crud_page("Playlists", "Playlists", "playlist_id", ["user_id"]))             # 4
        self.stack.addWidget(self.create_crud_page("Playlist_Songs", "Playlist Songs", "id", ["playlist_id", "song_id"])) # 5
        self.stack.addWidget(self.create_customer_song_page())     # 6

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)

    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("🎧 WELCOME TO MUSIC VIBE")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: darkgreen; margin: 30px;")

        pages = [
            ("Manage Users", 1),
            ("Manage Songs", 2),
            ("Manage Artists", 3),
            ("Manage Playlists", 4),
            ("Manage Playlist Songs", 5),
            ("🎵 View Customers & Songs", 6)
        ]

        for label, idx in pages:
            btn = QPushButton(label)
            btn.setStyleSheet("padding: 12px; font-size: 16px; background-color: #4CAF50; color: white; border-radius: 6px;")
            btn.clicked.connect(lambda _, x=idx: self.stack.setCurrentIndex(x))
            layout.addWidget(btn, alignment=Qt.AlignCenter)

        page.setLayout(layout)
        return page

    def create_crud_page(self, table, label, id_col, columns):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel(f"🔧 {label} CRUD Operations")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: black;")

        id_input = QLineEdit()
        id_input.setPlaceholderText(f"{id_col} (for update/delete)")
        inputs = [id_input]

        for col in columns:
            line = QLineEdit()
            line.setPlaceholderText(col)
            inputs.append(line)

        for input_widget in inputs:
            input_widget.setStyleSheet("padding: 6px; margin: 5px;")

        output = QTextEdit()
        output.setReadOnly(True)

        def get_values():
            return [inp.text() for inp in inputs[1:]]

        def clear_inputs():
            for i in inputs:
                i.clear()

        def add():
            try:
                question_marks = ",".join("?" for _ in columns)
                cursor.execute(f"INSERT INTO {table} ({','.join(columns)}) VALUES ({question_marks})", get_values())
                conn.commit()
                QMessageBox.information(self, "Success", "Record added successfully.")
                load()
                clear_inputs()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

        def update():
            try:
                set_expr = ", ".join(f"{col} = ?" for col in columns)
                values = get_values() + [id_input.text()]
                cursor.execute(f"UPDATE {table} SET {set_expr} WHERE {id_col} = ?", values)
                conn.commit()
                QMessageBox.information(self, "Success", "Record updated.")
                load()
                clear_inputs()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

        def delete():
            try:
                cursor.execute(f"DELETE FROM {table} WHERE {id_col} = ?", (id_input.text(),))
                conn.commit()
                QMessageBox.information(self, "Success", "Record deleted.")
                load()
                clear_inputs()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

        def load():
            output.clear()
            try:
                cursor.execute(f"SELECT * FROM {table}")
                for row in cursor.fetchall():
                    output.append(" | ".join(str(x) for x in row))
            except Exception as e:
                output.setText(f"Error: {e}")

        for btn_text, func in [("➕ Add", add), ("✏️ Update", update), ("❌ Delete", delete), ("🔄 Load All", load)]:
            btn = QPushButton(btn_text)
            btn.setStyleSheet("padding: 8px; font-weight: bold;")
            btn.clicked.connect(func)
            layout.addWidget(btn)

        layout.addWidget(title)
        for inp in inputs:
            layout.addWidget(inp)
        layout.addWidget(output)

        back_btn = QPushButton("🏠 Home")
        back_btn.setStyleSheet("padding: 8px; background-color: #607D8B; color: white; font-weight: bold; border-radius: 6px;")
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(back_btn)

        page.setLayout(layout)
        return page

    def create_customer_song_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("🎵 Customers & Their Songs")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: black;")

        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)

        load_btn = QPushButton("📄 Load Customers With Songs")
        load_btn.setStyleSheet("padding: 10px; background-color: #FF5722; color: white; font-weight: bold; border-radius: 6px;")
        load_btn.clicked.connect(self.load_customers_with_songs)

        home_btn = QPushButton("🏠 Home")
        home_btn.setStyleSheet("padding: 8px; background-color: #3F51B5; color: white; font-weight: bold; border-radius: 6px;")
        home_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        layout.addWidget(title)
        layout.addWidget(load_btn)
        layout.addWidget(self.output_area)
        layout.addWidget(home_btn)

        page.setLayout(layout)
        return page

    def load_customers_with_songs(self):
        self.output_area.clear()
        try:
            cursor.execute("""
                SELECT U.username, S.title
                FROM Users_new U
                JOIN Playlists P ON U.user_id = P.user_id
                JOIN Playlist_Songs PS ON P.playlist_id = PS.playlist_id
                JOIN Songs S ON PS.song_id = S.song_id
            """)
            for row in cursor.fetchall():
                self.output_area.append(f"Customer: {row[0]} | Song: {row[1]}")
        except Exception as e:
            self.output_area.setText(f"Error: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MusicApp()
    win.show()
    sys.exit(app.exec_())

