import tweepy
import keys
from operator import itemgetter

auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
auth.set_access_token(keys.access_token, keys.access_token_secret)

api = tweepy.API(auth)

nyc_trends = api.trends_place(id=23424848)
nyc_list = nyc_trends[0]['trends']
nyc_list = [t for t in nyc_list if t['tweet_volume']]

nyc_list.sort(key=itemgetter('tweet_volume'),reverse=True)

topics = {}

for trend in nyc_list:
    topics[trend['name']] = trend['tweet_volume']

from wordcloud import WordCloud
wordcloud = WordCloud(width=1600, height=900,
                           prefer_horizontal=0.5, min_font_size=10, colormap='prism',
                           background_color='white')

wordcloud = wordcloud = wordcloud.fit_words(topics)
wordcloud = wordcloud.to_file('TrendingTwitter.png')

