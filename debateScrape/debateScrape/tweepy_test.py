# Testing collection of data from Twitter
# For Donald Trump in this case

import tweepy
from tweepy import OAuthHandler
import json
import mysecrets

# Here I'm importing my API login details.
# If you're using your own login details, you can just replace them here.
# The Twitter API
sec = mysecrets.Secrets()
consumer_key = sec.consumer_key
consumer_secret = sec.consumer_secret
access_token = sec.access_token
access_secret = sec.access_secret

# This is some code that tweepy / the Twitter API needs to start a session
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

# Set how many times you want to fetch Tweets
# The reply will be 200 times this number
numberOfRuns = 1
allStatuses = []

# Set the ID of the last Tweet you want to fetch
maxId = 805804034309427200

# For each run in the range, fetch the tweets
for run in xrange(numberOfRuns):
    statuses = api.user_timeline('realDonaldTrump', max_id=maxId, count=5)
    for status in statuses:
        allStatuses.append(status)
    maxId = statuses[-1].id

# Save them all to files
with open('trumpStatusesSample.json','w') as f:
    json.dump([status._json for status in allStatuses], f)