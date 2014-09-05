#!/usr/bin/env python2
################################################################################
# RK_TwitterBot.py
#
# Authors: Ryan Jacobs and Kyle Domen
# https://github.com/ryanmjacobs/RK_TwitterBot
#
# v0.01 September 04, 2014: File creation.
# v0.02 September 04, 2014: Added 'Del Oro' functionality.
################################################################################

__version__ = "0.02"

import os, sys
from time import sleep
sys.path.append("./lib/oauthlib/")
sys.path.append("./lib/requests-oauthlib/")
sys.path.append("./lib/requests/")
sys.path.append("./lib/tweepy/")
import tweepy

# Put your API tokens here
consumer_key        = ""
consumer_secret     = ""
access_token        = ""
access_token_secret = ""

def bot_get(api):
    statuses = []

    for s in api.search(["Hate Del Oro"], count=1):
        statuses.append(s)

    return statuses

def bot_process(api, statuses, last_id):
    for s in statuses:
        status_id = s.id
        name      = s.user.screen_name
        text      = s.text
        print "\t@" + name + ": " + text

        if status_id == last_id:
            print "\tError: status_id is equal to the last id."
            return last_id

        try:
            reply = "@" + name + " You said, \"" + text + "\"... No you don't. You love Del Oro!"
            api.update_status(reply, status_id)
            print "\tReply: '" + reply + "'"
        except tweepy.TweepError as e:
            print "\tError", str(e.message[0]["code"]) + ":", e.message[0]["message"]

        return status_id

def countdown(string, seconds):
    for i in range(seconds, 0, -1):
        sys.stdout.write(string + ": %s  \r" % i)
        sys.stdout.flush()
        sleep(1)

def main():
    print os.path.basename(__file__) + " v" + __version__ + "\n"

    # Authorize to Twitter
    print "Twitter Authorization...",
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
        print "\nBot Name :", name + "\n"
    except:
        print "uh oh!"
        print "Couldn't get API. Quitting."
        sys.exit(1)

    # Begin Receive/Process Loop
    i=0
    last_id=0
    while True:
        i += 1
        print "Receive/Process Loop #" + str(i)

        statuses = bot_get(api)
        last_id = bot_process(api, statuses, last_id)
        countdown("Countdown", 60)

if __name__ == "__main__":
    main()
