import tweepy
import time
import requests
import nltk
import language_tool_python
import mysql.connector
import os

from os import environ
from datetime import datetime
from nltk.corpus import twitter_samples
from nltk.tag import pos_tag_sents

consumer_key = os.environ.get('twitterbot1_consumer_key')
consumer_secret = os.environ.get('twitterbot1_consumer_secret')

key = os.environ.get('twitterbot1_key')
secret = os.environ.get('twitterbot1_secret')

FILE_NAME = 'LastSeen.txt'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)


api = tweepy.API(auth)

def readLastSeen(FILE_NAME):
    fileRead = open(FILE_NAME,'r')
    lastSeenID = int(fileRead.read().strip())
    fileRead.close()
    return lastSeenID

def storeLastSeenID(FILE_NAME, lastSeenID):
    fileWrite = open(FILE_NAME,'w')
    fileWrite.write(str(lastSeenID))
    fileWrite.close()
    return

def follow(userID):
    if userID != 1389966788893581318:
        friendship = api.show_friendship(source_ID = 1389966788893581318, target_id=userID)
        #print(friendship[0].following)
        if friendship[0].following is False:
            api.create_friendship(userID)
    return

def followBack():
    followers = getFollowers()

    for person in followers:
        follow(person.id)
    return

def getSourceTweet(tweet):
    if tweet.is_quote_status is True:
        sourceTweet = api.get_status(id = tweet.quoted_status_id)
        #print(sourceTweet.user.id)
        follow(sourceTweet.user.id)
    else:
        if hasattr(tweet, 'retweeted_status'):
            #print(tweet.retweeted_status.user.id)
            follow(tweet.retweeted_status.user.id)
    return


def getTimeline():
    timelineTweets = api.home_timeline(since_id = readLastSeen(FILE_NAME), tweet_mode = 'extended')
    timelineText = []

    for tweet in reversed(timelineTweets):
        hypeMeUp(tweet)
        getSourceTweet(tweet)
        timelineText.append(tweet.full_text+"")
        storeLastSeenID(FILE_NAME,tweet.id)

    #print(timelineText)
    return timelineText

def postTweet(tweet):
    api.update_status(tweet)
    return

def getFollowers():
    followers = api.followers()
    #print(followers)
    #for person in followers:
        #print(person.id_str + " - "+ person.name)
    return followers

def hypeMeUp(tweet):
    #print(tweet.user.id)
    if '3228282473' in tweet.user.id_str and hasattr(tweet,'retweeted_status') is False:
        retweeters = api.retweeters(tweet.id)
        if 1389966788893581318 not in retweeters:
            api.retweet(tweet.id)
            api.create_favorite(tweet.id)
    return



def tweetsTokenizer(tweets):
    tweetsTokenized = []
    for tweet in tweets:
        tweetTokenized = nltk.word_tokenize(tweet)
        tweetsTokenized.append(tweetTokenized)
    return tweetsTokenized





#grammarCheck("Steve name car drive Big Red Orange My sport! Yes")
#followBack()
#getFollowers()
#getTimeline()

tweets = getTimeline()
print(tweets)


#db = mysql.connector.connect(
#    host="localhost",
#    user="root",
#    passwd= os.environ.get('local_sql_pass'),
#    database="TwitterBot1"
#)

#TwitterBotDB = db.cursor()
#TwitterBotDB.execute("CREATE TABLE Words (word VARCHAR(20), occurances int UNSIGNED, partofspeech VARCHAR(4), )")


#tweetsTokenized = nltk.word_tokenize(tweet for tweet in tweets)
#tweetsTokenized = tweetsTokenizer(tweets)
#print(tweetsTokenized)
#tweetsTagged = pos_tag_sents(tweetsTokenized)


#print(tweetsTagged)