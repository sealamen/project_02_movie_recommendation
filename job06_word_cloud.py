import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import collections
from konlpy.tag import Okt
from matplotlib import font_manager, rc
import matplotlib as mpl
import numpy as np

# colab에서 폰트적용
# fontpath = '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'
# font = font_manager.FontProperties(fname=fontpath, size=8)
# plt.rc('font', family='NanumBarunGothic')
# mpl.font_manager._rebuild()

# 파이참에서 폰트적용
font_path = './malgun.ttf'
font_name = font_manager.FontProperties(
    fname=font_path).get_name()
mpl.rcParams['axes.unicode_minus']=False
rc('font', family=font_name)

df = pd.read_csv('./crawling_data/cleaned_review_2015_2021.csv')
print(df.head())

# words = df[df['titles'] == '100% 울프: 푸들이 될 순 없어 (100% Wolf)']['cleaned_sentences']
# words = words[0].split()

words = df.iloc[1,1]
words = words.split()
print(words)

worddict = collections.Counter(words)
worddict = dict(worddict)
print(worddict)

# wordcloud 이미지 만들기
wordcloud_img = WordCloud(
    background_color = 'white', max_words=2000,
    font_path=font_path).generate_from_frequencies(worddict)

# wordcloud 이미지 그리기

plt.figure(figsize=(12,12))
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')
plt.show()

# stopwords 빼고 그리기
stopwords = ['영화', '감독', '개봉', '개봉일', '촬영', '관객', '관람', '주인공', '출연',
             '들이다', '푸다', '후원', '리뷰', '네이버']

from PIL import Image

movie_mask = np.array(Image.open('./crawling_data/movie_mask.jpg'))

wordcloud_img = WordCloud(
    background_color = 'white', max_words=2000,
    font_path=font_path, collocations=False, mask = movie_mask,
    stopwords=stopwords).generate(df.cleaned_sentences[0])

plt.figure(figsize=(12, 12))
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')
plt.show()