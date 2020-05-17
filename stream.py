#!/usr/bin/env python3
# Import required libraries
import json , time, datetime
from threading import Thread
from collections import deque
from collections import Counter
from twython import TwythonStreamer

#from requests.exceptions import ChunkedEncodingError



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

        # Tweets of tweets (total )
        self.total_tweets = 0

        # Tweets since last output
        self.iteration_tweets = 0
        self.emoji_tweets = 0

        self.hashtags = Counter()
        self.emojis = Counter()

    def add_tweet(self,tweet):
        # Increment
        self.total_tweets += 1
        self.iteration_tweets += 1

        self._hashtag_counts(tweet['entities']['hashtags'])
        self._emoji_counts(tweet['text'])

    # Increment hashtag counts
    def _hashtag_counts(self, hashtags):
        for hashtag in hashtags:
            self.hashtags.update({"{}".format(hashtag['text']): 1})

    def _emoji_counts(self,text):
        pass

    def output(self):
        current_time = datetime.datetime.now()

        processing_rate_current = int(self.iteration_tweets / int((current_time - self.iteration_timer).total_seconds()))
        processed_tweets = self.iteration_tweets
        self.iteration_tweets = 0
        self.iteration_timer = datetime.datetime.now()
        processing_rate_overall = int(self.total_tweets / int((current_time - self.start_timer).total_seconds()))

        out = {
            'datetime': current_time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            'total_tweets': self.total_tweets,
            'processing_rate_overall_rps': processing_rate_overall,
            'tweets_processed': processed_tweets,
            'processing_rate_current_rps': processing_rate_current,
            'top_emoji': self.emojis.most_common(10),
            'top_hashtags': self.hashtags.most_common(10),
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
        time.sleep(frequency)
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
