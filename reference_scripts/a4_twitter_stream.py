import twitter
import json

consumer_key = '' # deleted for security
consumer_secret = '' # deleted for security
access_token_key = '' # deleted for security
access_token_secret = '' # deleted for security

api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                  access_token_key=access_token_key, access_token_secret=access_token_secret)

# San Francisco coordinates
latlong = ["-122.75,36.8,-121.75,37.8"]

f = open('./twitter_streaming_data.json','w')
for tweet in api.GetStreamFilter(locations=latlong):
    f.write(json.dumps(tweet))
    f.write('\n')