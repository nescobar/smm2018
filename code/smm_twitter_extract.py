import json
import pandas as pd
import numpy as np
from sklearn.feature_extraction import text as sk_fe_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, f1_score, recall_score, accuracy_score
from TwitterAPI import TwitterAPI
from nltk import PorterStemmer, WordNetLemmatizer
from stopwords import STOPWORDS

consumer_key = 'cNXDNrP5cKh3tl6TEIsuJvV0m' # deleted for security
consumer_secret = '0MkPvk8PHK6hH5HhHLfeAZwgDJTbpk5iVtH1wbu31BGMFsaEDl' # deleted for security
access_token_key = '14079589-xSosB4T1aW66CzMJpyriVgYzjMyrabSeupmz1AkAc' # deleted for security
access_token_secret = '4z0IAlGdJdQqpSQuO3AO4F7rcVaHyVBBWwfSfespakiLc' # deleted for security

api = TwitterAPI(consumer_key, consumer_secret, auth_type='oAuth2')

def searchTwitter(query, maxid, feed="search/tweets",api=api,n=100):
    if maxid == 0:
        return [t for t in api.request(feed, {'q':query,'count':n})]
    else:
        return [t for t in api.request(feed, {'q': query, 'count': n, 'max_id': maxid})]

appended_tweets_df = []

minIdTweet_1 = 0    # Min ID Hastag 1
minIdTweet_2 = 0    # Min ID Hastag 2

# Get JSON from Twitter

# Loop over to collect tweets from Twitter
for i in range(20):
    tweets_1 = searchTwitter('#HurricaneHarvey', minIdTweet_1)
    tweets_2 = searchTwitter('#HarveyRelief', minIdTweet_2)

    # Convert the json returned by Twitter into a dataframe
    tweets_1_df = pd.read_json(json.dumps(tweets_1))
    tweets_2_df = pd.read_json(json.dumps(tweets_2))

    # Get min ID from dataframe
    minIdTweet_1 = tweets_1_df.loc[tweets_1_df['id'].idxmin()].id
    minIdTweet_2 = tweets_2_df.loc[tweets_2_df['id'].idxmin()].id                               

    # Append dataframe to existing one
    appended_tweets_df.append(tweets_1_df)
    appended_tweets_df.append(tweets_2_df)

# Concatenate dataframes
appended_tweets_df = pd.concat(appended_tweets_df)

# Drop duplicates
appended_tweets_df.drop_duplicates(subset=['id'], inplace=True)
appended_tweets_df.drop_duplicates(subset=['text'], inplace=True)

# Save to CSV
appended_tweets_df.to_csv(path_or_buf='/Users/nescobar/tweets_harvey_20180217.csv', encoding='utf-8')
