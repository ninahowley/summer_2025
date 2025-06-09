import sqlite3
import os

def connect_db():
    return sqlite3.connect("articles.db")

def init_db():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            domain TEXT,
            url TEXT,
            bias TEXT,
            credibility TEXT,
            reporting TEXT,
            content TEXT
        )
    ''')

def reset_db():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute('''
        DROP TABLE IF EXISTS articles
    ''')

def insert_page(conn, name:str, domain:str, url:str, bias:str, credibility:str, reporting:str, content:str) -> None:
    cur = conn.cursor()
    dupe = cur.execute("SELECT * FROM articles WHERE url = ?", (url,)).fetchone()
    if not dupe:
        cur.execute("INSERT INTO articles (name, domain, url, bias, credibility, reporting, content) VALUES (?, ?, ?, ?, ?, ?, ?)", (name, domain, url, bias, credibility, reporting, content,))
    else:
        print("This page is already in the database.")

def commit_changes(conn):
    conn.commit()

def close_db(conn):
    conn.close()

if __name__ == "__main__":
    init_db()

# reset_db()
# init_db()