# 여기서 할 일.
# 현재 4191개의 형태소별로 띄어쓰기된 문장이 있음
# 그 단어들을 싸그리 가져와서 BOW(Back of the Word)형태(그냥 빽에 막 들어가있는 느낌)
# 를 word2Vec 모델한테 줄거야(이미 만들어진 모델)
# Word2vec 모델은 모델의 첫 번째 레이어 embedding layer 같은 느낌이야
# 받은 모든 단어들에 축을 줘서 가까운데로 옮겨 그러면 단어의 갯수 만큼의 차원이 생기는 것이고
# 그만큼의 좌표가 생기는거야. 그러면 계산을 할 수 있게되지.

import pandas as pd
from gensim.models import Word2Vec

review_word = pd.read_csv('./crawling_data/cleaned_review_2015_2021.csv')
review_word.info()
print(review_word.loc[0])

cleaned_token_review = list(review_word['cleaned_sentences'])
# cleaned_sentence 컬럼만 잘라서 리스트로 바꿔서
# cleaned_token_review에 주면 리뷰 문장들의 리스트

print(cleaned_token_review[0])

cleaned_tokens = []
for sentence in cleaned_token_review:
    token = sentence.split() # split함수는 공백이 디폴트값
    cleaned_tokens.append(token)
    # 띄어쓰기 기준으로 잘랐으니 split하면 형태소 하나씩 따온 것을 리스트로 줌.
    # 그러니 여기서 append 하면 2차원, 더해면 1차원. 아래서 window 줘야하니까 2차원으로 받자
    # cleaned_tokens = cleaned_tokens + token
# print(cleaned_tokens)
print(token)
exit()
    # cleaned_token_review는 전처리된 형태소로 이루어진 한 영화의 리뷰
    # 그 중에 하나씩 들고와서 sentence

embedding_model = Word2Vec(cleaned_tokens, size=100,
                    window=4, min_count=20,
                    workers=4, iter=100, sg=1)
# 벡터라이징을 해주는 모델. 데이터를 줘서 학습을 시켜야해.
# 28421개의 형태소(아래서 출력하면 나와)니까 28421차원이겠지만,
# size를 100을 줘서 100차원 안에 형태소들을 다 넣는 것(차원을 축소)
# window는 예를 들어 형태소 10개짜리 문장이 있어. 얘를 학습하려면 4개씩 자르면서 이동하면 7번
# 20번 이하로 나오는 애들은 학습 안시키겠다(min_count=20)
# workers는 cpu의 코어 몇 개 쓸거냐. 작업관리자 > cpu > 코어 갯수만큼 주면 돼.

# gensim이 4.0 이상이면 size > vector_size, iter > epochs로 바꾸면 됨

# 학습이 된 모델을 임베딩 모델로 받음
# 임베딩 모델로 받으면 벡터화해서, 벡터간의 연산이 가능하게되어

embedding_model.save('./models/word2VedModel_2015_2021.model')
print(embedding_model.wv.vocab.keys())
print(len(embedding_model.wv.vocab.keys()))
# gensim 4.0 이상인 경우
# print(list(embedding_model.wn.index_to_key))
# print(len(list(embedding_model.wn.index_to_key)))

# print를 통해 키의 갯수를 보면 28,421개임을 확인할 수 있음.
