import config
import json
from requests_oauthlib import OAuth1Session

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

def get_tweets(**params) -> list:
  res = twitter.get(TL_URL, params = params)
  if res.status_code == 200:
    return json.loads(res.text)
  else:
    raise GetTweetsError(res.status_code)

def dump_tweets(**params):
  for line in get_tweets(**params):
    print(line['user']['name']+'::'+line['text'])
    print(line['created_at'])
    print('*******************************************')
