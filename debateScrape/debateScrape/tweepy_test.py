# Testing collection of data from Twitter
# For Donald Trump in this case

import tweepy
from tweepy import OAuthHandler
import json
import mysecrets

sec = mysecrets.secrets()
consumer_key = sec.consumer_key
consumer_secret = sec.consumer_secret
access_token = sec.access_token
access_secret = sec.access_secret

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

numberOfRuns = 1
allStatuses = []
maxId = 805804034309427200

for run in xrange(numberOfRuns):
    statuses = api.user_timeline('realDonaldTrump', max_id=maxId, count=5)
    for status in statuses:
        allStatuses.append(status)
    maxId = statuses[-1].id

with open('trumpStatusesSample.json','w') as f:
    json.dump([status._json for status in allStatuses], f)