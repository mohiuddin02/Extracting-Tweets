# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 11:40:16 2020

@author: mohiu
"""

import tweepy
import sys
import jsonpickle
import os
import json
import pandas as pd
import csv

print("1 started")

consumer_key = 
consumer_secret = 
access_key = 
access_secret = 

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth, wait_on_rate_limit=True,
				   wait_on_rate_limit_notify=True)

fName = 'tweets.json' 


sinceId = None
max_id = -10000
tweetCount = 0
alltweets = []

def collect_tweets(searchQuery,outtweets,max_id = -10000,tweetCount = 0):
    print("Downloading max {0} tweets".format(maxTweets))
    while tweetCount < maxTweets:
            try:
                if (max_id <= 0):
                    if (not sinceId):
                        new_tweets = api.search(q=searchQuery, count=tweetsPerQry, lang ='en')
                    else:
                        new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                                since_id=sinceId,lang ='en')
                else:
                    if (not sinceId):
                        new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                                max_id=str(max_id - 1),lang ='en')
                    else:
                        new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                                max_id=str(max_id - 1),
                                                since_id=sinceId,lang ='en')
                alltweets.extend(new_tweets)
                
                if not new_tweets:
                    print("No more tweets found")
                    break
                    #outtweets = ( [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets])
                outtweets = ( [[tweet.text, tweet.user.location] for tweet in alltweets])
                    # f.write(jsonpickle.encode(tweet._json, unpicklable=False) +'\n')
                tweetCount += len(new_tweets)
                print("Downloaded {0} tweets".format(tweetCount))
                max_id = new_tweets[-1].id
                
            except tweepy.TweepError as e:
                # Just exit if any error
                print("some error : " + str(e))
                break
    return outtweets


hashtags = pd.read_csv("hashtags.txt")
tags = hashtags["HASHTAGS"]
hastag = []
for x in range(len(tags)):
    text = tags[x]
    #text = text.strip('@')
    hastag.append(text)
    
#hastag = hastag[0:10]  
maxTweets = 10 #number tweets
tweetsPerQry = 200  #max 200


for x in range(len(hastag)):
    searchQuery = str(hastag[x])
    outtweets = []
    screen_name=collect_tweets(searchQuery, outtweets)
    data = pd.DataFrame(screen_name)
    screen_name = hastag[x]
    data.to_csv(f'test.csv', index=False)#data.to_csv(f'{x}_th_tag1.csv', index=False)
    data = pd.DataFrame()
