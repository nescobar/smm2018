import json

data_search = []

# Search data file
# Load the json from file into memory
print('\nSearch tweets file')
json_file = open('./twitter_search_data.json','r')
for line in json_file:
    data_search.append(json.loads(line))

# Check out the various keys for any one json object
print(data_search[0].keys())

# Try extract the tweets alone from this json dataset
tweets_search = []

for item in data_search:
    if 'text' in item.keys():
        tweets_search.append(item['text'])

print(tweets_search[0])

data_streaming = []
# Streaming data file
# Load the json from file into memory
print('\nStreaming tweets file')
json_file = open('./twitter_streaming_data.json','r')
for line in json_file:
    data_streaming.append(json.loads(line))

# Check out the various keys for any one json object
print(data_streaming[0].keys())

# Try extract the tweets alone from this json dataset
tweets_stream = []

for item in data_streaming:
    if 'text' in item.keys():
        tweets_stream.append(item['text'])

print(tweets_stream[0])
