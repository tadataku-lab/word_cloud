from get_tweets import save_tweets, remove_url
from word_cloud import get_word_cloud
import csv

fpath = "~/Library/Fonts/スマートフォントUI.otf"

params = {
  'exclude_replies': True,
  'include_rts': False,
  'count': 200
}

epoc = 1

save_tweets(epoc, **params)

texts = []
with open(f'./output/tweet_data{epoc * params["count"]}.csv', 'r') as f:
  reader = csv.reader(f, delimiter='\t')
  header = next(reader)

  for row in reader:
    texts += row

get_word_cloud(texts, fpath=fpath)
