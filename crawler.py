"""
A simple crawler to get all tweets of a particular user. Currently the tweet count
limit is 3200 for each user. This script will keep trying until it finishes. It reads
userids from a file and writes user specific JSON's to a specific directory.
Used as part of research project in class. This is probably based on some toy crawler
present in web mining books, don't remember. But that has been modified heavily for our purpose.
Optionally i can also get followers of a user and others whom a user follows.
"""
import io
import sys
import time
import json
import twitter
import logging
import datetime
from urllib2 import URLError
from httplib import BadStatusLine
from functools import partial
from sys import maxint

todayDate = []
today = datetime.date.today()
todayDate.append(today)

logging.basicConfig(filename='./companies/crawling_'+ str(todayDate[0]) + '.log',level=logging.DEBUG)
def oauth_login():
# connect to twitter api
	CONSUMER_KEY = 'Put your'
	CONSUMER_SECRET = 'twitter app keys'
	OAUTH_TOKEN = 'here. After you get the'
	OAUTH_TOKEN_SECRET = 'tokens from the website.'
	auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
	CONSUMER_KEY, CONSUMER_SECRET)
	twitter_api = twitter.Twitter(auth=auth)
	return twitter_api

def save_json(name, filename, data):
    with io.open('./companies/' + name + '/' + filename + '.json',
                 'w', encoding='UTF-8') as f:
        f.write(unicode(json.dumps(data, ensure_ascii=False)))
        noOfTweets = 0
        for line in data:
        	noOfTweets += 1
        if len(data):
          print "Got ",noOfTweets," tweets for ",data[0]['user']['id'], "of", name
          logging.info('Got %d tweets for %d of %s', noOfTweets, data[0]['user']['id'], name)

def load_json(directory, filename):
    with io.open('{0}/{1}.json'.format(directory,filename),
                 encoding='UTF-8') as f:
        return f.read()

def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw):

    def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):
        if wait_period > 3600: # Seconds
            print >> sys.stderr, 'Too many retries. Quitting.'
            raise e

        if e.e.code == 401:
            print >> sys.stderr, 'Encountered 401 Error (Not Authorized)'
            return None
        elif e.e.code == 404:
            print >> sys.stderr, 'Encountered 404 Error (Not Found)'
            return None
        elif e.e.code == 429:
            print >> sys.stderr, 'Encountered 429 Error (Rate Limit Exceeded)'
            logging.warning("Encountered 429 Error (Rate Limit Exceeded)")
            if sleep_when_rate_limited:
                print >> sys.stderr, "Retrying in 15 minutes...ZzZ..."
                logging.warning("Retrying in 15 minutes...ZzZ...")
                sys.stderr.flush()
                time.sleep(60*15 + 5)
                print >> sys.stderr, '...ZzZ...Awake now and trying again.'
                logging.warning("...ZzZ...Awake now and trying again.")
                return 2
            else:
                raise e # Caller must handle the rate limiting issue
        elif e.e.code in (500, 502, 503, 504):
            print >> sys.stderr, 'Encountered %i Error. Retrying in %i seconds' % \
                (e.e.code, wait_period)
            time.sleep(wait_period)
            wait_period *= 1.5
            return wait_period
        else:
            raise e

    wait_period = 2
    error_count = 0

    while True:
        try:
            return twitter_api_func(*args, **kw)
        except twitter.api.TwitterHTTPError, e:
            error_count = 0
            wait_period = handle_twitter_http_error(e, wait_period)
            if wait_period is None:
                return
        except URLError, e:
            error_count += 1
            print >> sys.stderr, "URLError encountered. Continuing."
            logging.debug("URLError encountered. Continuing.")
            if error_count > max_errors:
                print >> sys.stderr, "Too many consecutive errors...bailing out."
                raise
        except BadStatusLine, e:
            error_count += 1
            print >> sys.stderr, "BadStatusLine encountered. Continuing."
            if error_count > max_errors:
                print >> sys.stderr, "Too many consecutive errors...bailing out."
                raise

from functools import partial
from sys import maxint

# def get_friends_followers_ids(twitter_api, screen_name=None, user_id=None,
                              # friends_limit=maxint, followers_limit=maxint):
    # assert (screen_name != None) != (user_id != None), \
    # "Must have screen_name or user_id, but not both"
    # get_friends_ids = partial(make_twitter_request, twitter_api.friends.ids,
                              # count=5000)
    # get_followers_ids = partial(make_twitter_request, twitter_api.followers.ids,
                                # count=5000)

    # friends_ids, followers_ids = [], []
    # for twitter_api_func, limit, ids, label in [
                    # [get_friends_ids, friends_limit, friends_ids, "friends"],
                    # [get_followers_ids, followers_limit, followers_ids, "followers"]
                # ]:

        # if limit == 0: continue
        # cursor = -1
        # while cursor != 0:
            # # Use make_twitter_request via the partially bound callable...
            # if screen_name:
                # response = twitter_api_func(screen_name=screen_name, cursor=cursor)
            # else: # user_id
                # response = twitter_api_func(user_id=user_id, cursor=cursor)

            # if response is not None:
                # ids += response['ids']
                # cursor = response['next_cursor']

           # # print >> sys.stderr, 'Fetched {0} total {1} ids for {2}'.format(len(ids), label, (user_id or screen_name))
            # if len(ids) >= limit or response is None:
                # break

    # # Do something useful with the IDs, like store them to disk...
    # return friends_ids[:friends_limit], followers_ids[:followers_limit]

def harvest_user_timeline(twitter_api, screen_name=None, user_id=None, max_results=3200):
    assert (screen_name != None) != (user_id != None), \
    "Must have screen_name or user_id, but not both"

    kw = {  # Keyword args for the Twitter API call
        'count': 200,
        'trim_user': 'true',
        'include_rts' : 'true',
        'since_id' : 1,
        'verify' : 'false'
        }

    if screen_name:
        kw['screen_name'] = screen_name
    else:
        kw['user_id'] = user_id

    max_pages = 17
    results = []
    tweets = make_twitter_request(twitter_api.statuses.user_timeline, **kw)

    if tweets is None: # 401 (Not Authorized) - Need to bail out on loop entry
        tweets = []

    results += tweets
    page_num = 1

    if max_results == kw['count']:
        page_num = max_pages # Prevent loop entry

    while page_num < max_pages and len(tweets) > 0 and len(results) < max_results:
        kw['max_id'] = min([ tweet['id'] for tweet in tweets]) - 1
        tweets = make_twitter_request(twitter_api.statuses.user_timeline, **kw)
        results += tweets
        page_num += 1
    return results[:max_results]

twitter_api = oauth_login()
#read user ids for each company from a file and write to appropriate JSON file
companies = ['amazon', 'apple', 'cisco', 'dropbox', 'ebay', 'facebook', 'foursquare']
for name in companies:
  fp=open('./userids/' + name.strip() + ".txt", 'r')
  for eachline in fp:
	  eachline=eachline.strip()
	  #friends_ids, followers_ids = get_friends_followers_ids(twitter_api, screen_name=eachline, friends_limit=100, followers_limit=100)
	  #save_json(str,eachline + "_friends", friends_ids)
	  #save_json(str,eachline + "_followers",followers_ids)
	  tweets = harvest_user_timeline(twitter_api, screen_name=None, user_id=eachline, max_results=3200)
	  save_json(name, eachline, tweets)