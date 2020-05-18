#!/usr/bin/env python3
# Import required libraries
import json , datetime
from time import sleep
import emoji
from threading import Thread
from collections import deque
from collections import Counter
from twython import TwythonStreamer
from urllib.parse import urlparse


# Get Twitter Stream and Queue message to the Queue
class MyTwitterStream(TwythonStreamer):

    def __init__(self, consumer_key, consumer_secret, access_token, access_secret, msg_queue):
        self.tweet_queue = msg_queue
        super().__init__(consumer_key, consumer_secret, access_token, access_secret)

    def on_success(self, data):
        self.tweet_queue.append(data)

    def on_error(self, status_code, data, response_headers ):
        print(status_code)
        # Disconnect on error
        # TODO: add better error handling, to prevent exiting on recoverable errors.
        self.disconnect()

class TweetAnalytics():

    def __init__(self):
        # start timer from begining of time
        self.start_timer = datetime.datetime.now()

        # iteration timer , will reset at every output
        self.iteration_timer = datetime.datetime.now()

        # Tweet stat counters
        self.tweets_total = 0
        self.tweets_with_emoji = 0
        self.tweets_with_url = 0
        self.tweets_with_media=0

        # Tweets since last output
        self.tweets_iteration = 0

        # Track Top items in tweets
        self.hashtags = Counter()
        self.emojis = Counter()
        self.url_domains = Counter()

        self.media_type = Counter()

    def add_tweet(self,tweet):
        # Increment
        self.tweets_total += 1
        self.tweets_iteration += 1

        self._hashtag_counts(tweet['entities']['hashtags'])
        self._emoji_counts(tweet['text'])
        if 'media' in tweet['entities'].keys():
            self._media_counts(tweet['entities']['media'])
        self._url_counts(tweet['entities']['urls'])

    # Increment hashtag counts
    def _hashtag_counts(self, hashtags):
        for hashtag in hashtags:
            self.hashtags.update({ hashtag['text'] : 1})

    def _emoji_counts(self,text):
        if emoji.emoji_count(text) > 0:
            self.tweets_with_emoji += 1
            emoji_list = emoji.emoji_lis(text)
            for em in emoji_list:
                self.emojis.update({ emoji.demojize(em['emoji']) : 1 })

    def _url_counts(self,url_list):
        if len(url_list) > 0:
            self.tweets_with_url += 1
            domain_list = []
            for url in url_list:
                #Extract domain only
                domain_list.append( urlparse(url['expanded_url']).netloc )

            for domain in set(domain_list):
                self.url_domains.update({ domain : 1 })


    def _media_counts(self,media_list):
        if len(media_list) > 0:
            self.tweets_with_url += 1
            media_types=[]
            for item in media_list:
                media_types.append(item['type'])

            # Get unique items from the media list
            # This way each media only reported once per tweet
            for type in set(media_types):
                self.media_type.update({ type : 1 })

    def output(self):
        current_time = datetime.datetime.now()

        processing_rate_current = int(self.tweets_iteration / int((current_time - self.iteration_timer).total_seconds()) ) #TODO: avoid division by zero
        processed_tweets = self.tweets_iteration
        self.tweets_iteration = 0
        self.iteration_timer = datetime.datetime.now()
        processing_rate_overall = int( self.tweets_total / int((current_time - self.start_timer).total_seconds()) ) #TODO: avoid division by zero

        out = {
            'datetime': current_time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            'tweets_total': self.tweets_total,
            'tweets_with_url': self.tweets_with_url,
            'tweets_with_url_pct': int( 100 * self.tweets_with_url / self.tweets_total if self.tweets_total > 0 else 0 ), # avoid division by zero

            'tweets_with_emoji': self.tweets_with_emoji,
            'tweets_with_emoji_pct': int( 100 * self.tweets_with_emoji / self.tweets_total if self.tweets_total > 0 else 0 ), # avoid division by zero

            'tweets_with_media': self.tweets_with_media,
            'tweets_with_media_pct': int( 100 * self.tweets_with_media / self.tweets_total if self.tweets_total > 0 else 0 ), # avoid division by zero

            'processing_rate_overall_rps': processing_rate_overall,
            'tweets_processed_last': processed_tweets,
            'processing_rate_current_rps': processing_rate_current,

            'top_emoji': self.emojis.most_common(10),
            'top_hashtags': self.hashtags.most_common(10),
            'top_urls': self.url_domains.most_common(10),
            'top_media': self.media_type.most_common(10),

        }
        return json.dumps(out)

def process_tweets(tweets_queue, trends):
    while True:
        if len(tweets_queue) > 0:
            trends.add_tweet(tweets_queue.popleft())


# # Start the stream
def stream_tweets(tweets_queue):

    # Load credentials from json file
    #{
    #  "CONSUMER_KEY": "",  "CONSUMER_SECRET": "",
    #  "ACCESS_TOKEN": "", "ACCESS_SECRET": ""
    #}
    with open("credentials.json", "r") as file:
        creds = json.load(file)

    # Instantiate from our streaming class
    stream = MyTwitterStream(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'],
                         creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'],tweets_queue)

    # stream.statuses.sample(language='en')
    stream.statuses.sample(language='en')


def analytics_output(frequency,trends):
    while True:
        sleep(frequency)
        print(trends.output())


if __name__ == '__main__':

    # Create msg queue
    tweet_queue = deque()

    # Create tweeter stream injestion in another Thread
    tweet_stream = Thread(target=stream_tweets, args=(tweet_queue,), daemon=True)
    tweet_stream.start()

    trends = TweetAnalytics()

    # add options args to select how often you print rate_analytics
    #analytics_output(10,trends)
    terminal_logger = Thread( target=analytics_output, args=(10,trends,) )
    terminal_logger.start()


    # process tweets from the queue
    # TODO: use external queue system for publishing and processing of tweets
    process_tweets(tweet_queue,trends)
