import config
import json
from requests_oauthlib import OAuth1Session
import csv
from time import sleep

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

TL_URL = "https://api.twitter.com/1.1/statuses/user_timeline.json"

class GetTweetsError(Exception):
  """Exception raised for get tweets.

  Attributes:
      status_code -- a returned status code
  """

  def __init__(self, status_code):
    self.message = f'Getting tweets is failure! Status code is {status_code}.'
    self.status_code = status_code


def remove_url(tweet: str):
  return ''.join(filter(lambda s: not s.startswith('http'), tweet.split(' ')))


def get_tweets(epoc, **params) -> list:
  tweets = []
  for _ in range(epoc):
    res = twitter.get(TL_URL, params = params)
    if res.status_code == 200:
      limit = res.headers['x-rate-limit-remaining']
      print("API remain: " + limit)
      if limit == 1:
        sleep(60 * 15)
      tweets += json.loads(res.text)
      params['max_id'] = tweets[-1]['id'] - 1
    else:
      raise GetTweetsError(res.status_code)
  return tweets


def dump_tweets(epoc, **params):
  for line in get_tweets(epoc, **params):
    print(line['user']['name']+'::'+line['text'])
    print(line['created_at'])
    print('*******************************************')


def save_tweets(epoc, **params):
  with open(f'./output/tweet_data{epoc * params["count"]}.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(list(map(lambda tw: remove_url(tw['text']), get_tweets(epoc, **params))))
