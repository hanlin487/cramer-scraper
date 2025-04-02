import sqlite3 
import pandas
import psycopg2

def insert_to_tweets(df : pandas.DataFrame) -> None:
    conn = sqlite3.connect(f"../storage/tweets.db")
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

def sort_csv(filename : str, output : str) -> None:
    with open(f"../storage/{filename}") as f:
        lines = f.readlines()
        pairs = []

        for line in lines:
            line = line.strip().split(",")
            pairs.append([line[0], line[1:]])

        pairs = sorted(pairs, key=lambda x: x[0])
        
        new = open(f"../storage/{output}", "w")
        for pair in pairs:
            new.write(f"{pair[0]},{','.join(pair[1])}\n")

def remove_duplicates(filename : str, output : str) -> None:
    with open(f"../storage/{filename}") as f:
        lines = f.readlines()
        d = {}

        for line in lines:
            line = line.split(",")
            ticker = line[0]
            names = ",".join(line[1:]).strip()
            print(ticker, names)
            
            if ticker not in d:
                d[ticker] = names
        
        with open(f'../storage/{output}', "w") as new:
            for ticker, names in d.items():
                new.write(f"{ticker},{names}\n")

def connect_postgres():
    try:
        return psycopg2.connect(
            database="postgres",
            user="postgres",
            password="battleon9981",
            host="localhost",
            port="5432"
        )
    except Exception as e:
        print(f'Error with postgres connection: {e}')


if __name__ == "__main__":
    #postgres stuff
    conn = connect_postgres()
    if conn:
        print("Connected to postgres")
        conn.close()
    else:
        print('No connection')