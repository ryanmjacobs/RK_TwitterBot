#!/usr/bin/env python2
################################################################################
# RK_TwitterBot.py
#
# Authors: Ryan Jacobs and Kyle Domen
# https://github.com/ryanmjacobs/RK_TwitterBot
#
# v0.01 September 04, 2014: File creation.
################################################################################

__version__ = "0.01"

import os
import sys
import tweepy

# Put your API tokens here
consumer_key        = ""
consumer_secret     = ""
access_token        = ""
access_token_secret = ""

def bot_get():
    return statuses

def bot_process(statuses):
    return True

def main():
    print os.path.basename(__file__) + " v" + __version__ + "\n"

    # Authorize to Twitter
    print "Authorizing to Twitter...",
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    print "done!"

    # Check for good API
    print "Checking API...",
    try:
        name = api.me().name
        print "done!"
        print "\nBot Name :", name
    except:
        print "uh oh!"
        print "Couldn't get API. Quitting."
        sys.exit(1)

    statuses = bot_get()
    bot_process(statuses)

if __name__ == "__main__":
    main()
