from textblob import TextBlob
from transformers import pipeline
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
    
def pipeline_analyze_regular(tweet):
    sentiment_pipeline = pipeline("sentiment-analysis")
    return sentiment_pipeline(tweet)

def pipeline_analyze_financial(tweet):
    sentiment_pipeline = pipeline(model="ahmedrachid/FinancialBERT-Sentiment-Analysis")
    return sentiment_pipeline(tweet)

def blob_analyze(tweet):
    blob = TextBlob(tweet)
    if -0.2 < blob.sentiment.polarity < 0.2:
        return "neutral"
    elif blob.sentiment.polarity > 0.2:
        return "positive"
    else:
        return "negative"

def vader_analyze(tweet):
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(tweet)
    overall = scores['compound']
    # print(scores)

    if overall < -0.05:
        return "negative"
    elif overall > 0.05:
        return "positive"
    else:
        return "neutral"
    
def ngram_split(tweet):
    blob = TextBlob(tweet)
    return blob.ngrams(n=3)

# nltk.download("vader_lexicon")

txt = """
The tariffs are light, the introduction of them heavy
"""

grams = ngram_split(txt)
for gram in grams:
    data = " ".join(gram)
    blob_result = blob_analyze(data)
    vader_result = vader_analyze(data)
    hf_result1 = pipeline_analyze_regular(data)
    hf_result2 = pipeline_analyze_financial(data)

    print(f'\nstring : {data}\nblob : {blob_result}\nvader: {vader_result}\nhugging face base : {hf_result1}\nhugging face financial : {hf_result2}')

# while 1:
#     user_input = input("\nEnter input: ")
#     if user_input == "exit":
#         break
    
#     try:
#         pipe_result = 
#         vader_result = vader_analyze(user_input)
#         print(f'this tweet is {result} according to VADER')
#     except Exception as err:
#         print(f'Error in input {err}')
#         break
