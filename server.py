#!/usr/bin/env python3


#add the following
import os
import stat
import sys
import re
import requests
import string
import twitter
from requests_oauthlib import OAuth1

def postImage(src, auth): # returns media id
    ''' Posts a image to twitter's server, returns an image ID '''
    print("post image tweet")
    access_token = auth[0]
    access_token_secret = auth[1]
    consumer_key = auth[2]
    consumer_secret = auth[3]
    api = twitter.Api(consumer_key = consumer_key, consumer_secret = consumer_secret, access_token_key = access_token, access_token_secret=access_token_secret)
    return api.UploadMediaChunked(media=src)

def postTweetWithImage(image, status, auth, debug=False):
    ''' Posts a tweet using the requests library,
     along with an image uploaded with a prebuilt twitter library '''

    base_url = "https://api.twitter.com/1.1/statuses/update.json?"
    if debug:
        base_url = "localhost:9001"

    # extract Credentials
    access_token = auth[0]
    access_token_secret = auth[1]
    consumer_key = auth[2]
    consumer_secret = auth[3]

    # upload media
    image_id = postImage(image, auth)

    headers = {"Accept": "*/*", "Connection": "close", "User-Agent": "OAuth gem v0.4.4",\
     "Content-Type": "application/x-www-form-urlencoded", "status": status, "media_ids": image_id}

    if debug:
         r = requests.post("http://localhost:9001", data=headers)
         print(r.status_code, r.reason)
    else:
        rauth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
        r = requests.post("https://api.twitter.com/1.1/statuses/update.json?", data=headers, auth = rauth)
        print(r.status_code, r.reason)

def postTweet(status, auth, debug=False):
    ''' Posts a tweet using the requests library '''

    print("post regular tweet")
    sys.stdout.flush()

    # extract Credentials
    access_token = auth[0]
    access_token_secret = auth[1]
    consumer_key = auth[2]
    consumer_secret = auth[3]
    base_url = "https://api.twitter.com/1.1/statuses/update.json?"

    if debug:
        base_url = "localhost:9001"

    headers = {"Accept": "*/*", "Connection": "close", "User-Agent": "OAuth gem v0.4.4",\
     "Content-Type": "application/x-www-form-urlencoded", "status": status}

    if debug:
         r = requests.post("http://localhost:9001", data=headers)
         print(r.status_code, r.reason)
    else:
        rauth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
        r = requests.post("https://api.twitter.com/1.1/statuses/update.json?", data=headers, auth = rauth)
        print(r.status_code, r.reason)


if __name__ == '__main__':
    print("Type your tweet, or an image file followed by your tweet")
    tweet = input("")

    ## Setup Authentification ##

    # Personal Credentials
    access_token = #######################################
    access_token_secret = #######################################

    # Application Credentials
    consumer_key = #######################################
    consumer_secret = #######################################

    auth = [access_token, access_token_secret, consumer_key, consumer_secret]

    ## Setup Tweet ##
    # Check if tweet has an image file
    words = tweet.split(" ")
    first_word = words[0].lower()
    pattern = '.*(gif|jpg|jpeg|tiff|png)'

    if re.match(pattern, first_word, flags=0):
        # send a tweet with an image
        postTweetWithImage(first_word, words[1:], auth)
    else:
        # send a regular tweet
        postTweet(words[1:], auth)
