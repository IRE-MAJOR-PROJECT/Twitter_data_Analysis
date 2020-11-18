from tweetutilities import get_API

api = get_API()
tweets = []

counts = {'total_tweets': 0, 'locations':0}

from locationlistener import LocationListener
location_listener = LocationListener(api, counts_dict=counts,
                                     tweets_list=tweets, topic='trump', limit=10)

import tweepy

stream = tweepy.Stream(auth=api.auth, listener=location_listener)
stream.filter(track=['trump'], languages=['en'], is_async=False)

counts['total_tweets']
counts['locations']
print(f'{counts["locations"]/ counts["total_tweets"]:.1%}')

from tweetutilities import get_geocodes
bad_locations = get_geocodes(tweets)
#print(bad_locations)

from pandas import DataFrame
df = DataFrame(tweets)
df = df.dropna()
print(df)

import folium

usmap = folium.Map(location=[39.8283, -98.5795], tiles='Stamen Terrain',
                   zoom_start=5, detect_retina=True)

# Creating Popup Markers for the Tweet Locations
for t in df.itertuples():
     text = ': '.join([text])
     popup = folium.Popup(text, parse_html=True)
     marker = folium.Marker((a, b),
                            popup=popup)
     marker.add_to(usmap)

# Saving the Map
usmap.save('tweet_map.html')

#install folium library

# print(counts['total_tweets'])
# print(counts['locations'])
# print(f'{counts["locations"]/ counts["total_tweets"]:.1%}')

