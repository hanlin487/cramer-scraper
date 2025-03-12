import json
import tweepy
import os 
import pandas as pd
import storage
from dotenv import load_dotenv
from detection import detect_companies

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

# loads csv of SP500 companies into df {ticker : company name}
def load_sp500() -> pd.DataFrame:
    with open("../storage/companies.csv") as f:
        company_dict = {"ticker" : [], "names" : []}

        for line in f.readlines():
            line = line.strip().split(",")
            company_dict["ticker"].append(line[0])
            company_dict["names"].append(line[1:])

    companies = pd.DataFrame(company_dict)
    return companies

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
        
        # load the sp500
        sp500 = load_sp500()
        
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
                companies = detect_companies(tweet.text, sp500)
                companies = " ".join(companies)

                tweet_data = {
                    "tweet_id" : tweet.id,
                    "date" : str(tweet.created_at),
                    "content" : str(tweet.text),
                    "companies" : companies
                }
                tweets.append(tweet_data)
                count += 1
                if count >= num_of_tweets:
                    break
            if count >= num_of_tweets:
                break
    
        # setup df and return
        # print(f'TWEETS LIST {tweets}')
        df = pd.DataFrame(tweets).sort_values(by=["tweet_id"], ascending=True)
        return df
    
    except Exception as e:
        print(f"Error {str(e)}")

if __name__ == "__main__":    
    # if limit rated comment these 2 lines out
    # tweets = scrape_user(5)
    # storage.dataframe_to_csv(tweets)
    # tweets = pd.read_csv("../storage/tweets_from_scraping.csv").fillna("")
    