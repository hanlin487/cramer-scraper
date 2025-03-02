import sqlite3 
import pandas

def insert_to_db(df : pandas.DataFrame) -> None:
    conn = sqlite3.connect("./storage/tweets.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tweets (
            tweet_id TEXT PRIMARY KEY,
            date TEXT,
            content TEXT
        );
        """
    )
    cursor.executemany("INSERT INTO tweets (tweet_id, date, content) VALUES (?, ?, ?)", df.values.tolist())
    conn.commit()
    conn.close()

def clear_db() -> None:
    conn = sqlite3.connect('./storage/tweets.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tweets")
    conn.commit()
    conn.close()