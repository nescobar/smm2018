import twitter
import json

consumer_key = '' # deleted for security
consumer_secret = '' # deleted for security
access_token_key = '' # deleted for security
access_token_secret = '' # deleted for security

api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                  access_token_key=access_token_key, access_token_secret=access_token_secret)


# Search within a range of 5 kms of location provided (San Francisco)
# Keyword = love
# Result Type = recent
# Count = 500
f = open('./twitter_search_data.json','w')
results = api.GetSearch( raw_query="q=love%20&result_type=recent&count=100", geocode="-122.75,36.8,-121.75,37.8,5km")
for result in results:
    f.write(json.dumps(result.AsDict()))
    f.write('\n')

# json_results = [result.AsDict() for result in results]
# f.write(json.dumps(json_results))