#!/usr/bin/env python2
################################################################################
# RK_TwitterBot.py
#
# Authors: Ryan Jacobs and Kyle Domen
# https://github.com/ryanmjacobs/RK_TwitterBot
#
# v0.01 September 04, 2014: File creation.
# v0.02 September 04, 2014: Added 'Del Oro' functionality.
# v0.03 September 19, 2014: Added 'replying w/ image' functionality.
################################################################################

__version__ = "0.03"

import os, sys
import urllib, json
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
    statuses = api.user_timeline(username_goes_here, count=1)
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
            search_term = text.split(' ')[0]
            photo_url = google_image(search_term)
            if photo_url == "ERROR":
                reply = "Uh oh. Something went really wrong. Tell Ryan to fix his bug-filled code."
            else:
                reply = "@" + name + " Here's a photo of that: " + str(photo_url)
            api.update_status(reply, status_id)
            print "\tReply: '" + reply
        except tweepy.TweepError as e:
            print "\tError", str(e.message[0]["code"]) + ":", e.message[0]["message"]

        return status_id

def google_image(search_string):
    rest = "ERROR" # default return
    search = search_string.split()
    search = '%20'.join(map(str, search))
    url = 'http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=%s&safe=off' % search
    search_results = urllib.urlopen(url).read()
    try:
        js = json.loads(search_results.decode())
        results = js['responseData']['results']
        for i in results:
            rest = i['unescapedUrl']
    except:
        print "Error: couldn't read json"
    return rest

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
