import tweepy
import os 
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from dotenv import load_dotenv


def init_client():
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

def vader_analysis(text):
    nltk.download('vader_lexicon')
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text=text)

# def analyze(tweet):
#     analysis = TextBlob(tweet)

#     if analysis.sentiment.polarity > 0:
#         return 'positive'
#     elif analysis.sentiment.polarity == 0:
#         return 'neutral'
#     else:
#         return 'negative'

# return list of tweets
def scrape_user(num_of_tweets):
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
                # get sentiment 
                scores = vader_analysis(tweet.text)
                tweet_data = {
                    "date" : tweet.created_at,
                    "tweet_id" : tweet.id,
                    "sentiment" : scores,
                    "text" : tweet.text
                }
                tweets.append(tweet_data)
                count += 1
                if count >= num_of_tweets:
                    break
            if count >= num_of_tweets:
                break
    
        # setup df and return
        print(f'TWEETS LIST {tweets}')
        df = pd.DataFrame(tweets)
        # df = pd.DataFrame(sorted(tweets, key=lambda x: x["sentiment"]))
        filename = f"top{num_of_tweets}tweets_{username}.csv"
        df.to_csv(filename, index=False, mode='w')
        return df
        # return tweets
    
    except Exception as e:
        print(f"Error {str(e)}")

if __name__ == "__main__":
    num_of_tweets = int(input("Enter how many tweets to scrape, cannot exceed 100: "))
    tweets_df = scrape_user(num_of_tweets=num_of_tweets)
    print(tweets_df)