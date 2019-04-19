import tweepy  # pip3 install tweepy
import sys
import os
import json
import time


def criaJsonSaida(json_input):
    return {
        "id": json_input["id"],
        "data_criacao": json_input["created_at"],
        "text": json_input["text"],
        "nome_usuario": json_input["user"]["name"],
        "e_sobre_a_empresa": None
    }


api_key = ''
api_secret_key = ''

auth = tweepy.AppAuthHandler(api_key, api_secret_key)

api = tweepy.API(auth,
                 # Whether or not to automatically wait for rate limits to replenish
                 wait_on_rate_limit=True,
                 # Whether or not to print a notification when Tweepy is waiting for rate limits to replenish
                 wait_on_rate_limit_notify=True
                 )

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)


searchQuery = 'sadia'  # this is what we're searching for
maxTweets = 100000  # Some arbitrary large number
tweetsPerQry = 15  # this is the max the API permits
fName = 'tweets.json'  # We'll store the tweets in a text file.


# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1

dataset = {
    "tweets": []
}
tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))

while tweetCount < maxTweets:
    print(tweetCount)
    try:
        if (max_id <= 0):
            if (not sinceId):
                new_tweets = api.search(q=searchQuery,  # the search query string
                                        lang='pt-BR',
                                        count=tweetsPerQry)
            else:
                new_tweets = api.search(q=searchQuery,
                                        lang='pt-BR',
                                        count=tweetsPerQry,
                                        since_id=sinceId)
        else:
            if (not sinceId):
                new_tweets = api.search(q=searchQuery,
                                        lang='pt-BR',
                                        count=tweetsPerQry,
                                        max_id=str(max_id - 1))
            else:
                new_tweets = api.search(q=searchQuery,
                                        lang='pt-BR',
                                        count=tweetsPerQry,
                                        max_id=str(max_id - 1),
                                        since_id=sinceId)
        if not new_tweets:
            print("No more tweets found")
            break
        for tweet in new_tweets:
            tweetJson = criaJsonSaida(tweet._json)
            print(tweetJson)
            dataset["tweets"] += [tweetJson]
        tweetCount += len(new_tweets)
        max_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # Just exit if any error
        print("some error : " + str(e))
        break
with open(fName, 'w') as f:
    f.write(json.dumps(dataset, indent=2))

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))
