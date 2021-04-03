from TwitterAPI import TwitterAPI, TwitterRequestError, TwitterConnectionError
import json

#
# f = open("credentials.txt",'r')
#
# with open('credentials.txt') as f:
#     data = {}
#     for line in f:
#         key, value = line.strip().split('=')
#         data[key] = value
# print(data["consumer_key"])
api = TwitterAPI("","","","")

counter = 0
verified_tweets = 0
while True:
    try:
        iterator = api.request('statuses/filter', {'track':'bitcoin'}).get_iterator()  # get tweet
        crypto = ["btc", "bitcoin"] # keywords
        for item in iterator:
            tweet = item['text'].lower()  # make tweet text lowercase
            if item['user']['verified']:  # if tweet is from verified user
                for i in crypto:
                    if i in tweet:  # if keyword in the text of the tweet
                        verified_tweets += 1  # add to verified user counter
                        print(item)
                        break

            elif 'disconnect' in item:
                event = item['disconnect']
                if event['code'] in [2,5,6,7]:
                    # something needs to be fixed before re-connecting
                    raise Exception(event['reason'])
                else:
                    # temporary interruption, re-try request
                    break
            else:  # if tweet is from non verified user
                for i in crypto:
                    if i in tweet:
                        counter += 1
                        counter += verified_tweets  # add 1 and # verified tweets to overall counter
                        break
    except TwitterRequestError as e:
        if e.status_code < 500:
            # something needs to be fixed before re-connecting
            raise
        else:
            # temporary interruption, re-try request
            pass
    except TwitterConnectionError:
        # temporary interruption, re-try request
        pass


