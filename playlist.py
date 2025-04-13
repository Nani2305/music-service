import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Connect to SQLite database (creates db if not exists)
conn = sqlite3.connect("music_service.db")
cursor = conn.cursor()

# Create tables
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

# GUI Setup
root = tk.Tk()
root.title("Music Service Application")
root.geometry("800x600")

# Tabs
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Helper function to clear entry fields
def clear_entries(entries):
    for entry in entries:
        entry.delete(0, tk.END)

# Users Tab
frame_users = ttk.Frame(notebook)
notebook.add(frame_users, text='Users')

tk.Label(frame_users, text="Username").grid(row=0, column=0)
entry_username = tk.Entry(frame_users)
entry_username.grid(row=0, column=1)

tk.Label(frame_users, text="Email").grid(row=1, column=0)
entry_email = tk.Entry(frame_users)
entry_email.grid(row=1, column=1)

def add_user():
    username = entry_username.get()
    email = entry_email.get()
    if username and email:
        cursor.execute("INSERT INTO Users (username, email) VALUES (?, ?)", (username, email))
        conn.commit()
        messagebox.showinfo("Success", "User added successfully")
        clear_entries([entry_username, entry_email])
    else:
        messagebox.showerror("Error", "All fields required")

tk.Button(frame_users, text="Add User", command=add_user).grid(row=2, column=1, pady=10)

# Artists Tab
frame_artists = ttk.Frame(notebook)
notebook.add(frame_artists, text='Artists')

tk.Label(frame_artists, text="Name").grid(row=0, column=0)
entry_artist_name = tk.Entry(frame_artists)
entry_artist_name.grid(row=0, column=1)

tk.Label(frame_artists, text="Genre").grid(row=1, column=0)
entry_genre = tk.Entry(frame_artists)
entry_genre.grid(row=1, column=1)

tk.Label(frame_artists, text="Country").grid(row=2, column=0)
entry_country = tk.Entry(frame_artists)
entry_country.grid(row=2, column=1)

def add_artist():
    name = entry_artist_name.get()
    genre = entry_genre.get()
    country = entry_country.get()
    if name:
        cursor.execute("INSERT INTO Artists (name, genre, country) VALUES (?, ?, ?)", (name, genre, country))
        conn.commit()
        messagebox.showinfo("Success", "Artist added successfully")
        clear_entries([entry_artist_name, entry_genre, entry_country])
    else:
        messagebox.showerror("Error", "Name is required")

tk.Button(frame_artists, text="Add Artist", command=add_artist).grid(row=3, column=1, pady=10)

# Songs Tab
frame_songs = ttk.Frame(notebook)
notebook.add(frame_songs, text='Songs')

tk.Label(frame_songs, text="Title").grid(row=0, column=0)
entry_title = tk.Entry(frame_songs)
entry_title.grid(row=0, column=1)

tk.Label(frame_songs, text="Artist ID").grid(row=1, column=0)
entry_artist_id = tk.Entry(frame_songs)
entry_artist_id.grid(row=1, column=1)

tk.Label(frame_songs, text="Duration (sec)").grid(row=2, column=0)
entry_duration = tk.Entry(frame_songs)
entry_duration.grid(row=2, column=1)

tk.Label(frame_songs, text="Release Year").grid(row=3, column=0)
entry_release_year = tk.Entry(frame_songs)
entry_release_year.grid(row=3, column=1)

def add_song():
    title = entry_title.get()
    artist_id = entry_artist_id.get()
    duration = entry_duration.get()
    release_year = entry_release_year.get()
    if title and artist_id:
        cursor.execute("INSERT INTO Songs (title, artist_id, duration, release_year) VALUES (?, ?, ?, ?)",
                       (title, artist_id, duration, release_year))
        conn.commit()
        messagebox.showinfo("Success", "Song added successfully")
        clear_entries([entry_title, entry_artist_id, entry_duration, entry_release_year])
    else:
        messagebox.showerror("Error", "Title and Artist ID are required")

tk.Button(frame_songs, text="Add Song", command=add_song).grid(row=4, column=1, pady=10)

# Playlists Tab
frame_playlists = ttk.Frame(notebook)
notebook.add(frame_playlists, text='Playlists')

tk.Label(frame_playlists, text="User ID").grid(row=0, column=0)
entry_playlist_user = tk.Entry(frame_playlists)
entry_playlist_user.grid(row=0, column=1)

tk.Label(frame_playlists, text="Playlist Name").grid(row=1, column=0)
entry_playlist_name = tk.Entry(frame_playlists)
entry_playlist_name.grid(row=1, column=1)

tk.Label(frame_playlists, text="Description").grid(row=2, column=0)
entry_playlist_desc = tk.Entry(frame_playlists)
entry_playlist_desc.grid(row=2, column=1)

def add_playlist():
    user_id = entry_playlist_user.get()
    name = entry_playlist_name.get()
    desc = entry_playlist_desc.get()
    if user_id and name:
        cursor.execute("INSERT INTO Playlists (user_id, name, description) VALUES (?, ?, ?)",
                       (user_id, name, desc))
        conn.commit()
        messagebox.showinfo("Success", "Playlist created successfully")
        clear_entries([entry_playlist_user, entry_playlist_name, entry_playlist_desc])
    else:
        messagebox.showerror("Error", "User ID and Playlist Name are required")

tk.Button(frame_playlists, text="Create Playlist", command=add_playlist).grid(row=3, column=1, pady=10)

# Playlist-Songs Tab
frame_ps = ttk.Frame(notebook)
notebook.add(frame_ps, text='Add Songs to Playlist')

tk.Label(frame_ps, text="Playlist ID").grid(row=0, column=0)
entry_ps_playlist = tk.Entry(frame_ps)
entry_ps_playlist.grid(row=0, column=1)

tk.Label(frame_ps, text="Song ID").grid(row=1, column=0)
entry_ps_song = tk.Entry(frame_ps)
entry_ps_song.grid(row=1, column=1)

def add_song_to_playlist():
    playlist_id = entry_ps_playlist.get()
    song_id = entry_ps_song.get()
    if playlist_id and song_id:
        cursor.execute("INSERT INTO Playlist_Songs (playlist_id, song_id) VALUES (?, ?)", (playlist_id, song_id))
        conn.commit()
        messagebox.showinfo("Success", "Song added to playlist")
        clear_entries([entry_ps_playlist, entry_ps_song])
    else:
        messagebox.showerror("Error", "Playlist ID and Song ID are required")

tk.Button(frame_ps, text="Add Song to Playlist", command=add_song_to_playlist).grid(row=2, column=1, pady=10)

# Query Tab
frame_queries = ttk.Frame(notebook)
notebook.add(frame_queries, text='Queries')

result_box = tk.Text(frame_queries, height=15, width=90)
result_box.grid(row=1, column=0, columnspan=3)

def run_query():
    query = """
    SELECT p.name AS playlist, s.title AS song, a.name AS artist
    FROM Playlist_Songs ps
    JOIN Playlists p ON ps.playlist_id = p.playlist_id
    JOIN Songs s ON ps.song_id = s.song_id
    JOIN Artists a ON s.artist_id = a.artist_id
    ORDER BY p.name;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    result_box.delete('1.0', tk.END)
    for row in results:
        result_box.insert(tk.END, f"Playlist: {row[0]}, Song: {row[1]}, Artist: {row[2]}\n")

tk.Button(frame_queries, text="Show Playlist with Songs and Artists", command=run_query).grid(row=0, column=0, pady=10)

root.mainloop()

# Close DB connection on exit
conn.close()
