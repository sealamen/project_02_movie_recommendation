#===== 왕, 남자, 여왕, 여자의 벡터 ======
#     남자
# 왕       여자
#     여왕
# 왕 > 남자의 벡터값과 여왕 > 여자의 벡터값은 비슷해
# 마찬가지로 왕 > 여왕, 남자 > 여자의 벡터값도 비슷하다고 볼 수 있지.
# 근데 왕 > 남자, 왕 > 여왕의 벡터는 서로 관계가 없지
# ( 왕>남자>여자, 왕>여왕>여자의 벡터값으로 보면 의미를 찾을 수는 있겠지만, 낱개로는 무의미)
# 그렇게 관계가 있다 없다를 따지기 위해 코사인값을 봐.(삼각함수: 직각삼각형 변들의 비)
# 코사인(끼인각) = 밑변(x)/빗변(t)
# 그렇다면 각도로 봤을 때,
# 두 벡터가 같은 방향(0도) : 유사하다
# 두 벡터가 다른 방향(180도): 반대된다
# 두 벡터가 직각(90도): 관계없다

# 각도가 작다면(0에 가깝다면) 빗변과 밑면의 길이가 거의 비슷하지(1에 가까워져)
# 각도가 90도에 가깝다면 코사인 값이 0에 가까워져.(x(밑변)이 0인 셈이니까)
# 각도가 180도에 가깝다면 x(밑변)이 음수가 되잖아. -1에 가까워져.(반지름 1짜리 원을 그려봐)

# 그래서 코사인 유사도는
# 1에 가까울 수록 유사하다. 0에 가까울 수록 관계가 없다. -1에 가까우면 반대되는 의미다


import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmwrite, mmread
import pickle
from gensim.models import Word2Vec

# 데이터 가져오기
df_reviews = pd.read_csv('./crawling_data/cleaned_review_2015_2021.csv')
Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

# tocsr()을 줘야 인덱싱이 가능함

# 영화를 10개 추천해주는 함수(코사인 유사도들을 주면 그중에 가장 큰 거 10개 뽑아줘)
def getRecommendation(cosine_sim):
    simScore = list(enumerate(cosine_sim[-1]))
    simScore = sorted(simScore, key=lambda x:x[1],
                      reverse=True)
    simScore = simScore[1:11]
    movieidx = [i[0] for i in simScore]
    recMovieList = df_reviews.iloc[movieidx]
    return recMovieList
# cosine_sim은 다른 영화리뷰들과의 코사인 유사도값들을 담은 리스트(2겹임(2차원))
# enumerate 했으니 그 값들에 0,1,2...4191 숫자가 붙겠지. 곧 영화의 인덱스 값이겠지.
# 이렇게 코사인 유사도값과 enumerate한 인덱스를 리스트로 준 것이 simScore
# 그 다음에 정렬(sorted). enumerate 을 한 이유는 정렬하면 인덱스가 무너지니까
# 정렬은 코사인 유사도값을 기준으로(simScore[1]), reverse=True는 내림차순(앞에 큰 값들)
# 그중에 1번부터 10번까지를 봤어. (0번은 값이 1일거고 자기 자신일 것이니까 안봐)
# movieidx는 simScore의 0번 인덱스. 즉 아까 enumerate에서 준 인덱스
# movieidx를 가지고 iloc해서 가장 유사한 영화제목 10개를 리턴해주는거야.

# 아래에 예시가 있음



# # # 영화 제목/ index를 이용한 추천
# #
# # # 해당 이름의 영화의 index를 가져오기.
# movie_idx = df_reviews[df_reviews['titles']=='트랜짓 (Transit)'].index[0]
# print(movie_idx)
# # 정확한 영화 제목을 줘야해.
# # 앞에서 전처리해서 동일한 제목은 하나밖에 없겠지만 혹시모르니 첫번째 꺼(index[0])
# # .index[0] 을 안주면 인덱스만 나오지 않고 인덱스, title, review까지 다 출력됨
#
# # # n번째 영화를 가져오고 싶다
# # movie_idx = 10
# # print(df_reviews.iloc[movie_idx, 0])
# # 10번째 영화를 추천받고 싶다.
# # 10번째 영화의 0번(title)을 뽑아내면 됨
#
#
# cosine_sim = linear_kernel(Tfidf_matrix[movie_idx],
#                            Tfidf_matrix)
# print(cosine_sim)
# print(cosine_sim[0])
# print(len(cosine_sim[0]))
# # linear_kernel에 tfidf_matrix[인덱스 값]과 다른 matrix 값들을 주면 일일이 코사인을 계산해줌
# # 따라서 cosine_sim에는 다른 영화들과의 cosine 값들을 다 입력해놓은 리스트를 출력
#
# recommendation = getRecommendation(cosine_sim)
# print(recommendation.iloc[:,0])
# # 그래서 getRecommendation한테 cosine_sim을 주면 유사한 영화 10개를 리턴해줘
# # 0번인덱스(titles)를 싹다[:] 출력하겠다.


# key_word를 통한 영화추천

embedding_model = Word2Vec.load('./models/word2VedModel_2015_2021.model')
# 유사단어를 찾으려면 word2vec 모델이 있어야겠죠. 여기에 단어를 하나 줄 것.
key_word = '토르'
sentence = [key_word] * 11     # sentence는 '토르'가 11번 들어있는 리스트
sim_word = embedding_model.wv.most_similar(key_word, topn=10)
# most_similar를 쓰면 유사단어 찾기. key_word 기준으로 10개. 그걸 words로 받아

words = []
for word, _ in sim_word:
    words.append(word)
print(words)
# sim_word는 앞에는 단어, 뒤에는 유사도로 되어있음. 우린 여기서 단어만 받을 것
# words에는 key_word의 유사단어 10개가 들어있을 것
# 이제 이걸 가지고 문장을 만들어줄거야


for i, word in enumerate(words):
    sentence += [word] * (10-i)
sentence = ' '.join(sentence)
print(sentence)
# sentence는 현재 keyword가 11번 반복된 상태. 그 다음으로 유사한 단어는 10번, 그 다음 9번..
# 이런 식으로 붙여서 문장을 만들거야. 왜냐면 tfidf는 문장 내의 단어의 반복 정도를 통해서
# 유사도를 찾아내기 때문에. 유사한 단어일수록 더 많이 반복되도록


sentence_vec = Tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
recommendation = getRecommendation(cosine_sim)
print(recommendation['titles'])
# tfidf 이전에 저장 해놓은 것을 그대로 불러왔으므로 fit_transform이 아닌 transform
# linear_kernel에 sentence_vec 값과 매트릭스 값을 주면 일일이 코사인 값을 계산해줄 것
# 그걸 가지고 getRecommendation에 주고 titles를 출력해보자

# 그럼 우리가 문장을 줄 수도 있겠지. ex) '지옥'의 한줄 평을 가져와 sentence로 주고
# 추천을 해줄 수도 있겠지.
