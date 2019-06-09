import MeCab
from wordcloud import WordCloud

mecab = MeCab.Tagger()

stop_words = {u'てる', u'いる', u'なる', u'れる', u'する', u'ある', u'こと', u'これ', u'さん', u'して',
              u'くれる', u'やる', u'くださる', u'そう', u'せる', u'した', u'思う',
              u'それ', u'ここ', u'ちゃん', u'くん', u'', u'て', u'に', u'を', u'は', u'の', u'が', u'と', u'た', u'し', u'で',
              u'ない', u'も', u'な', u'い', u'か', u'ので', u'よう', u'', 
              u'今日', u'明日', u'昨日', u'時間', u'最近', u'自分', u'気持ち', u'みたい', u'とき', u'わけ', u'すぎ', u'ところ', u'みんな', u'久しぶり', u'わり', u'好き', u'せい', u'もの', u'sarah', u'com', u'sarahah', u'Sarahah'}

def texts2words(texts: list):
  words = []
  for text in texts:
    for word_info in mecab.parse(text).split('\n'):
      if word_info == 'EOS': break
      word, info = word_info.split('\t')
      if (info.split(',')[0] == '名詞') and (info.split(',')[1] != 'サ変接続'):
        words.append(word)
  return words


def get_word_cloud(texts: list, path="./output/wordcloud.png", fpath=None):
  wordcloud = WordCloud(background_color="white", stopwords=stop_words,
                        font_path=fpath, width=900, height=500).generate(' '.join(texts2words(texts)))
  wordcloud.to_file(path)

