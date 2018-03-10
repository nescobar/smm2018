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

def score(true,pred):
  return (precision_score(true,pred),
          recall_score(true,pred),
          f1_score(true,pred),
          accuracy_score(true,pred))

def write_to_json(results):
    f = open('./harvey_data/harvey_data_20180217.json', 'w')
    for result in results:
        f.write(json.dumps(result.AsDict()))
        f.write('\n')

def normalize(x,style="PorterStemmer"):
  """This normalizer will remove stopwords and normalize text"""
  x = [t.lower() for t in x.split() if t not in STOPWORDS]
  if style == "PorterStemmer":
    return " ".join(list(map(PorterStemmer().stem,x)))
  elif style == "Lemma":
    return " ".join(list(map(WordNetLemmatizer.lemmatize,x)))
  elif style == "CharGram":
    cs = " ".join(x)
    return " ".join([cs[i:i+3] for i in range(0,len(cs),3)])
  else:
    return " ".join(x)

def print_score(s):
  print("""Precision:  {:0.3} Recall:     {:0.3} F-Score:    {:0.3}  Accuracy:    {:0.3} """.format(*s))

def searchTwitter(query, maxid, feed="search/tweets",api=api,n=100):
    if maxid == 0:
        return [t for t in api.request(feed, {'q':query,'count':n})]
    else:
        return [t for t in api.request(feed, {'q': query, 'count': n, 'max_id': maxid})]

#twitter_text = []

appended_tweets_df = []

minIdTweet_1 = 0    # Min ID Hastag 1
minIdTweet_2 = 0    # Min ID Hastag 2

#Get JSON from Twitter

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
#appended_dogs_d = pd.concat(appended_dogs_d)

# Drop duplicates
appended_tweets_df.drop_duplicates(subset=['id'], inplace=True)
appended_tweets_df.drop_duplicates(subset=['text'], inplace=True)
#appended_dogs_d.drop_duplicates(subset=['id'], inplace=True)

# Save to CSV
#appended_tweets_df.columns=['user','created_at','favorited','retweets','text']
appended_tweets_df.to_csv(path_or_buf='/Users/nescobar/tweets_harvey_20180217.csv', encoding='utf-8')



# Get a sample of 2500 each, dogs and cats (5000 in total)
appended_tweets_df = appended_tweets_df.sample(2500)
#appended_dogs_d = appended_dogs_d.sample(2500)

# Get text only and replace hashtags with blanks
tweets_text = [x.replace('#cats',"") for x in appended_cats_d['text']]
#dogs_text = [x.replace('#dogs',"") for x in appended_dogs_d['text']]

# Normalize texts
cats_text_nrm = [normalize(x) for x in cats_text]
dogs_text_nrm = [normalize(x) for x in dogs_text]

# Create features and return sparse matricies
vectorizer = sk_fe_text.CountVectorizer(dogs_text_nrm+dogs_text_nrm)
vectorizer.fit(dogs_text_nrm+dogs_text_nrm)
cats_tdm = vectorizer.transform(cats_text_nrm).toarray()
dogs_tdm = vectorizer.transform(dogs_text_nrm).toarray()

# Create visible matricies and combine
zeros = np.zeros((len(cats_text_nrm),1))
ones = np.ones((len(dogs_text_nrm),1))
catsdogs = np.concatenate((cats_tdm,dogs_tdm),axis=0)
y = np.ravel(np.concatenate((zeros,ones),axis=0))

#Create train/test split for modeling
trainX,testX,trainY,testY = train_test_split(catsdogs,y,test_size=.20)

#Naive Bayes
from sklearn.naive_bayes import GaussianNB
nb = GaussianNB()
nb.fit(trainX,trainY)

print("\n\nNaive Bayes Performance")
s = score(testY,nb.predict(testX))
print_score(s)

#SVM
from sklearn.svm import SVC
svm = SVC()
svm.fit(trainX,trainY)

print("\n\nSVM performance")
s = score(testY,svm.predict(testX))
print_score(s)

#Neural Network
from sklearn.neural_network import MLPClassifier
nn = MLPClassifier()
nn.fit(trainX,trainY)

print("\n\nNeural Network Performance")
s = score(testY,nn.predict(testX))
print_score(s)

#KNN
from sklearn.neighbors import KNeighborsClassifier
knn1 = KNeighborsClassifier(n_neighbors=1)
knn5 = KNeighborsClassifier(n_neighbors=5)
knn5d = KNeighborsClassifier(n_neighbors=5,weights='distance')

knn1.fit(trainX,trainY)
knn5.fit(trainX,trainY)
knn5d.fit(trainX,trainY)

print("\n\nKNN 1 Neighbor Performance")
s = score(testY,knn1.predict(testX))
print_score(s)

print("\n\nKNN 5 Neighbor Performance")
s = score(testY,knn5.predict(testX))
print_score(s)

print("\n\nKNN 5 Neighbor Weighted Performance")
s = score(testY,knn5d.predict(testX))
print_score(s)
