import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread
import pickle

# tfidf는 문장단위로 벡터화를 한다고 생각하면돼.
# Word2vec은 단어의 갯수만큼 차원이 생겼잖아. 얘는 마찬가지로 문장의 갯수만큼의 차원이 생겨
df_reviews = pd.read_csv('./crawling_data/cleaned_review_2015_2021.csv')
df_reviews.info()

Tfidf = TfidfVectorizer(sublinear_tf=True)
Tfidf_matrix = Tfidf.fit_transform(df_reviews['cleaned_sentences'])
# 단어의 반복을 통해 문장의 유사도를 찾아줌
# 단어의 빈도가 비슷하면 비슷한 문장이라고 판단하는 것
# 대신 모든 문장에 있는 단어면 같이가지고있어도 오히려 감점.

with open('./models/tfidf.pickle', 'wb') as f:
    pickle.dump(Tfidf, f)

mmwrite('./models/Tfidf_movie_review.mtx', Tfidf_matrix)

# matrix
# 예를 들어서 문장이 100개가 있어. 0번 문장과 1번 문장의 tfidf값이 얼마냐
# 이거를 99번문장까지하면 0번문장의 벡터값 100개가 나오겠지, 그다음 1번문장도 100개...
# 이런 식으로 모든 문장에 대해서 100개씩 좌표를 구해 그러면 100*100개의 매트릭스가 만들어져
# 이것이 tfidf 매트릭스. 이걸 저장할 때 scipy에 있는 input, oupput함수를 사용하면 좋아
# 저장할 때는 mmwrite, 읽어올 때는 mmread. mm은 matrix market


