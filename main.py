import json
import re
import tweepy
import os 
import pandas as pd
import nltk
import sqlite3
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from dotenv import load_dotenv

# init tweepy client
def init_client() -> None:
    load_dotenv()
    bearer_token = os.getenv("BEARER_TOKEN")
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_key_secret = os.getenv("CONSUMER_KEY_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
    client = tweepy.Client(
                        bearer_token=bearer_token,
                        consumer_key=consumer_key,
                        consumer_secret=consumer_key_secret,
                        access_token=access_token,
                        access_token_secret=access_token_secret,
                        wait_on_rate_limit=True
                        )
    return client

# loads csv of SP500 companies into dictionary {ticker : company name}
def load_csv() -> dict:
    with open('companies.csv') as file:
        companies = {}
        tickers = set()
        names = set()
        lines = file.readlines()

        for line in lines:
            line = line.strip('\n').split(',')
            companies[line[0]] = line[1:]
            tickers.add(line[0])

            for n in line[1:]:
                names.add(n) if n else None
    
    return (dict(sorted(companies.items())), tickers, names)

# scrapes tweets
def scrape_user(num_of_tweets) -> pd.DataFrame:
    # boot up tweepy client for twitter
    username = "jimcramer"
    client = init_client()
    
    try:    
        # get jimcramer user
        user = client.get_user(username=username)
        if not user.data:
            raise ValueError(f"User {username} not found")
        
        # get necessary info and set up paginator to pull multiple tweets
        user_id = user.data.id
        tweets = []
        paginator = tweepy.Paginator(
            client.get_users_tweets,
            id=user_id,
            max_results=num_of_tweets,
            tweet_fields=["text", "public_metrics", "created_at"],
        )

        # load tweets from paginator iterable into simple tweets_data list to put into df
        count = 0
        for batch in paginator:
            if not batch.data:
                break
        
            for tweet in batch.data:
                tweet_data = {
                    "tweet_id" : tweet.id,
                    "date" : tweet.created_at,
                    "text" : tweet.text
                }
                tweets.append(tweet_data)
                count += 1
                if count >= num_of_tweets:
                    break
            if count >= num_of_tweets:
                break
    
        # setup df and return
        # print(f'TWEETS LIST {tweets}')
        df = pd.DataFrame(tweets)
        return df
    
    except Exception as e:
        print(f"Error {str(e)}")

# saves dataframe to csv
def save_to_csv(df) -> None:
    filename = f"top{len(df)}tweets_jimcramer.csv"
    df.to_csv(filename, index=False, mode='w')

def insert_to_db(df) -> None:
    conn = sqlite3.connect("tweets.db")
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
    conn = sqlite3.connect('tweets.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tweets")
    conn.commit()
    conn.close()

def find_companies():
    

if __name__ == "__main__":
    # num_of_tweets = int(input("Enter how many tweets to scrape, cannot exceed 100: "))
    # tweets_df = scrape_user(num_of_tweets=num_of_tweets)
    testdf = pd.read_csv("top10tweets_jimcramer.csv")
    testdf = testdf[['tweet_id', 'date', 'text']]

    # TODO tokenize tweets and detect companies in each tweet if exists ************************************************************************************