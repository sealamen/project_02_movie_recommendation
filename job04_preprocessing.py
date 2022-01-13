import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./crawling_data/naver_movie_reviews_onesentence_2015_2021.csv')
# print(df['reviews'].head())
# print(df.reviews.head())
# exit()

okt = Okt()

stopwords = pd.read_csv('./crawling_data/stopwords.csv', index_col=0)
# stopwords 데이터는 인덱스가 있으므로 index_col=0을 주자
# stopwords_list = list(stopwords['stopword'])
# stopwords_movie = ['영화', '감독', '개봉', '개봉일', '촬영', '관객', '관람', '주인공', '출연',
#              '들이다', '푸다', '후원', '리뷰', '네이버']


# # 아래에서 stopword 못지워서(아래쪽 불용어 처리부분 수정 완료)
# # 파일 다시 불러와서 여기서 지우자. 불러오는김에 index도 죽이자.
# df2 = pd.read_csv('./crawling_data/cleaned_review_2015_2021.csv', index_col=0)
# cleaned_sentences = []
# print(df2)
# # exit()
# for cleaned_sentence in df2.cleaned_sentences:
#     cleaned_sentence_words = cleaned_sentence.split()
#     words = []
#     for word in cleaned_sentence_words:
#         if word not in list(stopwords['stopword']):
#             words.append(word)
#     cleaned_sentence = ' '.join(words)
#     cleaned_sentences.append(cleaned_sentence)
# df2['cleaned_sentences'] = cleaned_sentences
# df2.to_csv('./crawling_data/cleaned_review_2015_2021.csv', index=False)
# exit()


# sub 확인: 가-힣 제외 사라진 것 확인 가능
# print(df.loc[0,'reviews'])
# print(re.sub('[^가-힣 ]', ' ', df.loc[0, 'reviews']))

# token 확인: 명사, 동사, 형용사, 이런 식으로 나눠져
# sentence = re.sub('[^가-힣 ]', ' ', df.loc[0, 'reviews'])
# print(sentence)
# token = okt.pos(sentence, stem=True)
# print(token)

count = 0
cleaned_sentences = []
for sentence in df.reviews:   # df.reviews하면 데이터프레임의 reviews 컬럼만 가져와.
    count += 1
    if count % 10 == 0:
        print('.', end='')
    if count % 100 == 0:
        print()
    # count는 진행상황을 보기 위함.
    # 10개마다 점을 하나 찍고, 100개마다 엔터를 칠 것
    sentence = re.sub('[^가-힣 ]', '', sentence)
    # sentence에서 한글과 띄어쓰기 빼고 다 없애.
    token = okt.pos(sentence, stem=True)
    # okt.pos를 하면 품사까지 같이 받아줘(형태소, 품사를 튜플 쌍으로 갖는 리스트로 줌)
    # stem=True를 주면 어간의 원형으로 가져와(먹었습니다. 먹었지 등등 다 먹다 라는 원형 + 으니 이렇게옴
    # token은 리스트(형태소, 품사가 튜플로 들어있음)

    # 명사(Noun), 동사(Verb), 부사(Adjective)만 남기자
    df_token = pd.DataFrame(token, columns=['word', 'class'])
    df_cleaned_token = df_token[(df_token['class'] == 'Noun') |
                                (df_token['class'] == 'Verb') |
                                (df_token['class'] == 'Adjective')]
    # 1글자, 불용어 처리
    words = []
    for word in df_cleaned_token['word']:
        if len(word) > 1:
            if word not in list(stopwords['stopword']):
                words.append(word)
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)

df['cleaned_sentences'] = cleaned_sentences
print(df.head())
df.info()
df = df[['titles', 'cleaned_sentences']]
# 총 세 개의 컬럼 중에서 2개만 갖고 저장해. 아래처럼 reviews를 drop해도 되긴하지
# df.drop('reviews', inplace=True, axis = 1)
df.to_csv('./crawling_data/cleaned_review_2015_2021.csv', index=False)

