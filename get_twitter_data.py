
from __future__ import absolute_import, print_function

import tweepy
import time
import logging
import simplejson as json
import jsonpickle

#Keys must be obtained from apps.twitter.com
#My Personal api keys have been omitted
consumer_key= ""
consumer_secret= ""
access_token= ""
access_token_secret= ""

#Authenticataion to access twitter
#Via Tweepy documentation
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#prints to console, for debugging purposes
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')

if (not api):
    logging.error("Can't Authenticate")
    sys.exit(-1)

auth.secure = True
logging.warning("Script Authenticated.")

fields = "screen_name id_str".split() #array of strings

logging.warning("Obtaining my friend data...")
for user in tweepy.Cursor(api.friends).items():
    #Omit Twitter users/pages/celebrities with high follower:following ratio
    if ((user.followers_count/user.friends_count) > 1):
        continue
    logging.warning("Obtaining "+ user.screen_name +"'s data")
    json_user = json.loads(jsonpickle.encode(user._json))
    tw_user = {}
    for f in fields:
        tw_user[f] = ""   #set the keys in the tweeter dictionary
        tw_user[f] = json_user[f]
    print (tw_user)
    friend_list = []
    try:
        #Get follower ids of my friends
        #Use Tweepy Cursor Pagination to minimize Rate Limit Errors
        logging.warning("Obtaining "+ user.screen_name +"'s followers' ids")
        for page in tweepy.Cursor(api.followers_ids, screen_name = tw_user['screen_name']).pages():
            friend_list.extend(page)
            print (page)
            time.sleep(90) #Staggers api calls

    except tweepy.TweepError:
        data = api.rate_limit_status()
        logging.warning(json.dumps(data, indent=4, sort_keys=True))
        logging.warning(": Sleeping...")
        time.sleep(60 * 15)
        logging.warning(": Resuming...")
        continue
