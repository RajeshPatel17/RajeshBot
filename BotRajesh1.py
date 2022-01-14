import tweepy
import time
import requests
import nltk
import language_tool_python
import mysql.connector
import os

from os import environ
from datetime import datetime
from nltk.tag import pos_tag
from nltk.tokenize import TweetTokenizer

consumer_key = os.environ.get('twitterbot1_consumer_key')
consumer_secret = os.environ.get('twitterbot1_consumer_secret')

key = os.environ.get('twitterbot1_key')
secret = os.environ.get('twitterbot1_secret')

FILE_NAME = 'LastSeen.txt'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)

def readLastSeen(FILE_NAME): # reads last seen tweetId from local file
    fileRead = open(FILE_NAME,'r')
    lastSeenID = int(fileRead.read().strip())
    fileRead.close()
    return lastSeenID

def storeLastSeenID(FILE_NAME, lastSeenID): #stores last seen tweetId from local file
    fileWrite = open(FILE_NAME,'w')
    fileWrite.write(str(lastSeenID))
    fileWrite.close()
    return

def follow(userID): # will follow users that RajeshBot is not following
    if userID != 1389966788893581318:
        friendship = api.show_friendship(source_ID = 1389966788893581318, target_id=userID)
        if friendship[0].following is False:
            api.create_friendship(userID)
    return

def followBack(): # will follow users that are following RajeshBot
    followers = getFollowers()
    for person in followers:
        follow(person.id)
    return

def getSourceTweet(tweet): #Gets source tweet (used in case of retweets)
    if tweet is None: 
        return None
    if hasattr(tweet, 'retweeted_status') and not hasattr(tweet, 'quoted_status'):
        return api.get_status(id = tweet.retweeted_status.id)
    if hasattr(tweet, 'quoted_status'):
        return api.get_status(id = tweet.quoted_status_id)
    return tweet

def followTweeter(tweet):#follows user who tweeted said tweet
    follow(tweet.user.id)
    return
    
def getTimelineTweets(): #Gets timeline and returns all tweets
    tweets = api.home_timeline(since_id= readLastSeen(FILE_NAME), tweet_mode='extended')
    returnedtweets = []
    for tweet in reversed(tweets):
        storeLastSeenID(FILE_NAME,tweet.id)
        ogtweet = getSourceTweet(tweet)
        hypeMeUp(ogtweet)
        followTweeter(ogtweet)
        returnedtweets.append(ogtweet)
    return returnedtweets

def getTimelineText(): #gets timeline of RajeshBot to LastSeenTweet
    timelineTweets = api.home_timeline(since_id = readLastSeen(FILE_NAME), tweet_mode = 'extended')
    timelineText = []
    for tweet in reversed(timelineTweets):
        hypeMeUp(tweet)
        getSourceTweet(tweet)
        timelineText.append(tweet.full_text+"")
        storeLastSeenID(FILE_NAME,tweet.id)
    return timelineText

def postTweet(tweet): #will post tweet with text passed in parameter
    api.update_status(tweet)
    return

def getFollowers(): #gets all followers of RajeshBot
    followers = api.followers()
    return followers

def hypeMeUp(tweet): #Likes and retweets tweet from my main account
    if '3228282473' in tweet.user.id_str and hasattr(tweet,'retweeted_status') is False:
        retweeters = api.retweeters(tweet.id)
        if 1389966788893581318 not in retweeters:
            api.retweet(tweet.id)
            api.create_favorite(tweet.id)
    return


def tweetsTagger(tweets): #Tokenizes and tags the tweets
    from nltk.tokenize import TweetTokenizer
    tweetsTagged = []
    for tweet in tweets:
        text = ""
        if hasattr(tweet, 'full_text'):
            text = str(tweet.full_text)
        else:
            text = str(tweet.text)
        print(text)
        tt = TweetTokenizer()
        tweetTokenized = tt.tokenize(text.replace("’","'"))
        print(tweetTokenized)
        tweetTagged = pos_tag(tweetTokenized)
        tweetsTagged.append(tweetTagged)
    return tweetsTagged


tweets = getTimelineTweets()

#db = mysql.connector.connect(
#    host="localhost",
#    user="root",
#    passwd= os.environ.get('local_sql_pass'),
#    database="TwitterBot1"
#)

#TwitterBotDB = db.cursor()
#TwitterBotDB.execute("CREATE TABLE Words (word VARCHAR(20), occurances int UNSIGNED, partofspeech VARCHAR(4), )")


tweetsTagged = tweetsTagger(tweets)
print(tweetsTagged)