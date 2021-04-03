from TwitterAPI import TwitterAPI
import json

f = open("credentials.txt",'r')

with open('credentials.txt') as f:
    data = {}
    for line in f:
        key, value = line.strip().split('=')
        data[key] = value
print(data["consumer_key"])
api = TwitterAPI(data["consumer_key"],data["consumer_secret"],data["access_token_key"], data["access_token_secret"])

counter = 0

while True:
    try:
        iterator = api.request('statuses/filter', {'track':'bitcoin'}).get_iterator()

        for item in iterator:

            if True:
            # if item['verified'].lower() == "true":
            #     print("hi")
            # print(item['text'])
            # print(item["verified"])
                crypto = ["btc", "bitcoin"]
                tweet = item['text'].lower()
                for i in crypto:
                    if i in tweet:

                        counter += 1
                        print(counter)
                        break

            elif 'disconnect' in item:
                event = item['disconnect']
                if event['code'] in [2,5,6,7]:
                    # something needs to be fixed before re-connecting
                    raise Exception(event['reason'])
                else:
                    # temporary interruption, re-try request
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
