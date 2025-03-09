import sqlite3 
import pandas

def insert_to_db(df : pandas.DataFrame) -> None:
    conn = sqlite3.connect("../storage/tweets.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tweets (
            tweet_id TEXT PRIMARY KEY,
            date TEXT,
            content TEXT,
            companies TEXT
        );
        """
    )
    cursor.executemany("INSERT OR IGNORE INTO tweets (tweet_id, date, content, companies) VALUES (?, ?, ?, ?)", df.values.tolist())
    conn.commit()
    conn.close()

def clear_db() -> None:
    conn = sqlite3.connect('../storage/tweets.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tweets")
    conn.commit()
    conn.close()

def dataframe_to_csv(df : pandas.DataFrame) -> None:
    df.to_csv("../storage/tweets_from_scraping.csv", index=False)

def database_to_csv() -> None:
    conn = sqlite3.connect('../storage/tweets.db')
    cursor = conn.cursor()
    cursor.execute("select * from tweets")
    data = cursor.fetchall()
    df = pandas.DataFrame(data, columns=["tweet_id", "date", "content", "companies"])
    df.to_csv("../storage/tweets_saved_in_db.csv", index=False)