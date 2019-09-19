# import the libraries
# tweepy - twitter api wrapper
# collections - easy dictionary manipulation
# urlparse - get domain names
# regular expression - get words minus punctuation from sentences
# threading/ time - non-blocking processing + timer
# copy - too deep copy items
# sys - fetching cmd arguments
# keys - get twitter api keys
import tweepy
from tweepy import OAuthHandler
from collections import defaultdict
from urllib.parse import urlparse
import re
from threading import Thread
import time
from copy import copy
import sys
from keys import *


# thread class for handling reports every minute
class ReportGenerator(Thread):
    def __init__(self, print_report):
        super().__init__()
        self.print_report = print_report
        self.is_done = False

    def run(self):
        global limit
        # queue for data fetched as per the limit
        track = []
        while not self.is_done: 
            time.sleep(self.print_report)

            item = (copy(TweetListener.usernames), TweetListener.urls_count, copy(TweetListener.urls), copy(TweetListener.final_words))
            track.append(item)

            # resetting the variables for newer data to be entered
            TweetListener.urls_count = 0
            TweetListener.usernames = defaultdict(int)
            TweetListener.urls = defaultdict(int)
            TweetListener.final_words = defaultdict(int)

            print("************************************ REPORT ************************************")

            urls_count = 0
            usernames = defaultdict(int)
            urls = defaultdict(int)
            words = defaultdict(int)
            for item in track:
                urls_count += item[1] 

                for key, val in item[0].items():
                    usernames[key] += val

                for key, val in item[2].items():
                    urls[key] += val

                for key, val in item[3].items():
                    words[key] += val



            print("USERNAME REPORT")
            for username in usernames:
                print(username,":", usernames[username])

            print("LINK REPORT")
            print("Total number of links: ", str(urls_count))
            sorted_urls = sorted(urls.items(), key=lambda k_v: k_v[1], reverse=True)
            for url in sorted_urls:
                print(url[0],":", url[1])

            print("WORDS REPORT")
            print("Total number of unique words: ", str(len(words)))
            print("Top 10 words used are:")
            sorted_words = sorted(words.items(), key=lambda k_v: k_v[1], reverse=True)[:10]
            print(sorted_words)

            # removing data that is no longer required for the report
            if len(track) == limit:
                track.pop(0)

            


# class that extends from StreamListener
# contains functions for report generation
class TweetListener(tweepy.StreamListener):
    # initializations
    urls_count = 0
    usernames = defaultdict(int)
    urls = defaultdict(int)
    stop_words = {'a', 'an', 'the', 'of', 'in', 'am', 'are', 'as', 'at', 'be', 'do', 'did', 'for', 'from', 'have', 'has', }
    final_words = defaultdict(int)
    t = ReportGenerator(60)
    t.start()

    def on_status(self, status):
        print("tweet")
        self.generateReport(status)     

    def on_error(self, status_code):
        if status_code == 420:
            return False
        else:
            print("Error, status code encountered: ", str(status_code))

    def generateReport(self, status):
        self.generateUsernames(status.user.screen_name)
        self.generateLinks(status.entities['urls'])
        self.generateWords(status.text)

    def generateUsernames(self, username):
        self.usernames[username] += 1

    def generateLinks(self, links):
        for link in links:
            TweetListener.urls_count += 1
            self.urls[urlparse(link['expanded_url']).netloc] += 1

    def generateWords(self, text):
        words = re.findall(r'\w+', re.sub(r'https://t.co\S+', '', text))
        for word in words:
            if word.lower() not in self.stop_words:
                TweetListener.final_words[word.lower()] += 1


if __name__ == "__main__":
    keyword = sys.argv[1]
    limit = sys.argv[2]
    if limit == "one":
        limit = 1
    elif limit == "five":
        limit = 5
    else:
        print("Invalid Limit... going for default")
        limit = 1

    # authentication and authorization
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    # initializing the listener
    listener = TweetListener()
    tweetStream = tweepy.Stream(auth, listener)

    # filtering on the given word
    tweetStream.filter(track=[keyword], is_async=True)

