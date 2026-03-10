import sqlite3

def create_connection():
    return sqlite3.connect("quiz.db")

def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        score INTEGER NOT NULL,
        percentage REAL NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def insert_score(name, difficulty, score, percentage):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO scores (name, difficulty, score, percentage)
        VALUES (?, ?, ?, ?)
    """, (name, difficulty, score, percentage))

    conn.commit()
    conn.close()

def get_top_scores():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, difficulty, score, percentage
        FROM scores
        ORDER BY percentage DESC
        LIMIT 5
    """)

    results = cursor.fetchall()
    conn.close()
    return results