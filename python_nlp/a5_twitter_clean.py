import json
import re
import html
import nltk
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import stopwords
from nltk.tag import pos_tag

data_search = []

# Load the json from file into memory
json_file = open('./twitter_streaming_data.json','r')
for line in json_file:
    data_search.append(json.loads(line))

# Try extract the tweets alone from this json dataset
tweets_search = []

for item in data_search:
    if 'text' in item.keys():
        tweets_search.append(item['text'])

# Dictionary with patterns
dict_patterns = {"[,]" : "",        # Remove punctuations
                "http\S+" : "",     # Remove URLs
                 "@\S+" : "",       # Remove usernames

                 # Remove apostrophe's and expand words
                 "\\b[Ii]['’][Ll][Ll]\\b" : "I will",
                 "[Tt]['’][Ss]\\b" : "t is",
                 "\\b[Ii]['’][v][e]\\b" : "I have",
                 "\\b[Ww][Ee]['’][Vv][Ee]\\b" : "we have",
                 "\\b[Yy]['’][Aa][Ll][Ll]\\b" : "you all",
                 "\\b[Cc][Aa][Nn]['’][Tt]\\b" : "can not",
                 "\\b[Dd][Ii][Dd]['’][Tt]\\b" : "did not",
                 "\\b[Dd][Oo][Nn]['’][Tt]\\b" : "do not",
                 "\\b[Ii]['’][Mm]\\b" : "I am",

                 #  Word patterns for formatting
                "\\b[Gg][Uu][Dd]\\b" : "good", # gud
                 "\\b[Ll][Uu][Vv]\\b" : "love", # luv
                 "\\b[Bb][Rr][Oo]\\b" : "brother", # bro
                 "\\b[Cc][Uu][Dd]\\b" : "could", # cud
                 "\\b[Hh][Aa][Vv]\\b" : "have", # hav
                 "\\b[Ww][Aa][Tt]\\b" : "what", # wat
                 "\\b[Gg][Ii][Vv]\\b" : "give", # giv

                  "#\S+" : ""       # Remove hashtags
                 }

# Load stopwords
stop = stopwords.words('english')

pos_tweets = 0
neg_tweets = 0
neu_tweets = 0

####################################
# 1. Clean up tweets
####################################

for tweet in tweets_search:

    # Parse HTML
    #print(tweet)
    tweet_v0 = html.unescape(tweet)

    tweet_v1 = ""
    for k, v in dict_patterns.items():
        apost_pattern = re.compile(k)
        if tweet_v1 == "":
            tweet_v1 = re.sub(apost_pattern, v, tweet_v0)
        else:
            tweet_v1 = re.sub(apost_pattern, v, tweet_v1)

    print(tweet_v1)

    ####################################
    # 2. Calculate polarity of tweets
    ####################################
    tweet_non_stop = []

    # Tokenize tweet
    tokens = nltk.tokenize.word_tokenize(tweet_v1)

    # Exclude stopwords
    for word in tokens:
        if word not in stop:
            tweet_non_stop.append(word)

    # Get POS (Part of Speech) to use in polarity calculation
    tweet_pos = pos_tag(tweet_non_stop)

    pos_dict = {"NN":'n', "VBP":'v', "JJ":'a', "RB":'r'}

    pscore = 0
    nscore = 0
    # Calculate polarity of each word
    for k, v in tweet_pos:
        if v in pos_dict:
            scores = list(swn.senti_synsets(k, pos_dict[v]))
            if len(scores) > 0:
                pscore += scores[0].pos_score()
                nscore += scores[0].neg_score()
            # If word is not in sentiwordnet lexicon then it will not affect score
        else:
            scores = list(swn.senti_synsets(k))
            if len(scores) > 0:
                pscore += scores[0].pos_score()
                nscore += scores[0].neg_score()
            # If word is not in sentiwordnet lexicon then it will not affect score

    if pscore > nscore:
        print("Positive tweet")
        pos_tweets+=1
    elif nscore > pscore:
        print("Negative tweet")
        neg_tweets += 1
    else:
        print("Neutral tweet")
        neu_tweets += 1

print("\n########")
print("SUMMARY")
print("########")
print("There were ", pos_tweets, " positive tweets ", neg_tweets, " negative tweets and ", neu_tweets, " neutral tweets")
