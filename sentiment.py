from textblob import TextBlob
from transformers import pipeline
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

def pipe_analyze(tweet):
    pipe = pipeline("sentiment-analysis")
    print(pipe(tweet))
    
def vader_analyze(tweet):
    nltk.download("vader_lexicon")
    sia = SentimentIntensityAnalyzer()
    print(sia.polarity_scores(tweet))

txt = """
“I think that it’s a great company. I do think that there’s a lot of people who believe that they will not be able to deliver on this quarter. I, therefore, am reluctant to get in ahead of the quarter and we did sell the stock a little bit higher for the charitable trust”
"""

# pipe_analyze(txt)
vader_analyze(txt)