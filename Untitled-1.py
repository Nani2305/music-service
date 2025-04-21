
# Step 1: Import required libraries
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Step 2: Connect to SQLite database
conn = sqlite3.connect("music_service.db")
cursor = conn.cursor()

# Step 3: Create tables if not exists
cursor.executescript('''
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Artists (
    artist_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    genre TEXT,
    country TEXT
);

CREATE TABLE IF NOT EXISTS Songs (
    song_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist_id INTEGER,
    duration INTEGER,
    release_year INTEGER,
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id)
);

CREATE TABLE IF NOT EXISTS Playlists (
    playlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS Playlist_Songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    playlist_id INTEGER,
    song_id INTEGER,
    FOREIGN KEY (playlist_id) REFERENCES Playlists(playlist_id),
    FOREIGN KEY (song_id) REFERENCES Songs(song_id)
);
''')
conn.commit()

# Step 4: Setup GUI
root = tk.Tk()
root.title("Music Service Application")
root.geometry("900x600")
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Step 5: Create Users tab
users_tab = ttk.Frame(notebook)
notebook.add(users_tab, text='Users')

tk.Label(users_tab, text="Username:").grid(row=0, column=0)
username_entry = tk.Entry(users_tab)
username_entry.grid(row=0, column=1)

tk.Label(users_tab, text="Email:").grid(row=1, column=0)
email_entry = tk.Entry(users_tab)
email_entry.grid(row=1, column=1)

def add_user():
    username = username_entry.get()
    email = email_entry.get()
    if username and email:
        cursor.execute("INSERT INTO Users (username, email) VALUES (?, ?)", (username, email))
        conn.commit()
        messagebox.showinfo("Success", "User added successfully")
    else:
        messagebox.showerror("Error", "Please enter all fields")

tk.Button(users_tab, text="Add User", command=add_user).grid(row=2, column=1)

# Step 6: Create Artists tab
artists_tab = ttk.Frame(notebook)
notebook.add(artists_tab, text='Artists')

tk.Label(artists_tab, text="Name:").grid(row=0, column=0)
artist_name_entry = tk.Entry(artists_tab)
artist_name_entry.grid(row=0, column=1)

tk.Label(artists_tab, text="Genre:").grid(row=1, column=0)
genre_entry = tk.Entry(artists_tab)
genre_entry.grid(row=1, column=1)

tk.Label(artists_tab, text="Country:").grid(row=2, column=0)
country_entry = tk.Entry(artists_tab)
country_entry.grid(row=2, column=1)

def add_artist():
    name = artist_name_entry.get()
    genre = genre_entry.get()
    country = country_entry.get()
    if name:
        cursor.execute("INSERT INTO Artists (name, genre, country) VALUES (?, ?, ?)", (name, genre, country))
        conn.commit()
        messagebox.showinfo("Success", "Artist added successfully")
    else:
        messagebox.showerror("Error", "Please enter the artist name")

tk.Button(artists_tab, text="Add Artist", command=add_artist).grid(row=3, column=1)

# Step 7: Run GUI
root.mainloop()

# Step 8: Close database connection
conn.close()
