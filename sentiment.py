import json
from textblob import TextBlob
from transformers import pipeline
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
    
def hf_regular(tweet):
    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    return sentiment_pipeline(tweet)

# prosusai model https://huggingface.co/ProsusAI/finbert?text=Stocks+rallied+and+the+British+pound+gained.
def hf_financial_prosus(tweet):
    sentiment_pipeline = pipeline(model="ProsusAI/finbert")
    return sentiment_pipeline(tweet)

#distilroberta financial model https://huggingface.co/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis
def hf_financial_roberta(tweet):
    sentiment_pipeline = pipeline(model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
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

def regular_analysis(text):
    blob_result = blob_analyze(text)
    vader_result = vader_analyze(text)
    hf_result1 = hf_regular(text)
    hf_result2 = hf_financial_prosus(text)
    hf_result3 = hf_financial_roberta(text)
    
    results = {
        "blob" : blob_result,
        "vader" : vader_result,
        "hugging face base" : hf_result1,
        "hugging face prosus" : hf_result2,
        "hugging face roberta" : hf_result3
    }
    # print(f'\nstring : {data}\nblob : {blob_result}\nvader: {vader_result}\nhugging face base : {hf_result1}\nhugging face prosus : {hf_result2}\nhugging face roberta : {hf_result3}')    
    return results

def ngram_analysis(text):
    grams = ngram_split(text)
    results = {}
    for gram in grams:
        data = " ".join(gram)

        blob_result = blob_analyze(data)
        vader_result = vader_analyze(data)
        hf_result1 = hf_regular(data)
        hf_result2 = hf_financial_prosus(data)
        hf_result3 = hf_financial_roberta(data)

        results[data] = {
            "blob" : blob_result,
            "vader" : vader_result,
            "hugging face base" : hf_result1,
            "hugging face prosus" : hf_result2,
            "hugging face roberta" : hf_result3
            }
        # print(f'\nstring : {data}\nblob : {blob_result}\nvader: {vader_result}\nhugging face base : {hf_result1}\nhugging face prosus : {hf_result2}\nhugging face roberta : {hf_result3}')
    return results

txt = """
The relentless selling in Nvidia is a sign, once again, or the weak shareholder base that only knows it is a hot stock not that it is a great company, plus worries about a potential Taiwan sellout by President Trump
"""

res = regular_analysis(txt)
print(json.dumps(res, indent=4))