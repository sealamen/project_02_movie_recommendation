# Word2Vec embedding model의 시각화
# 2차원으로 차원축소를해서 평면에다 표현해볼 것

import pandas as pd
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.manifold import TSNE         # 차원축소를 해주는 애
from matplotlib import font_manager, rc   # 한글 폰트를 사용하므로
import matplotlib as mpl

# 폰트 적용하기
font_path = './malgun.ttf'
font_name = font_manager.FontProperties(
    fname=font_path).get_name()
mpl.rcParams['axes.unicode_minus']=False
rc('font', family=font_name)


# 저장했던 embedding모델 가져오기
embedding_model = Word2Vec.load('./models/word2VedModel_2015_2021.model')
key_word = '여름'
sim_word = embedding_model.wv.most_similar(key_word, topn=10)
print(sim_word)
# most_similar를 쓰면 학습시킨 단어들 중 유사한 단어 top n가지를 뽑아내
# simword를 print해보면 단어와 유사도(높을수록 유사)가 나옴.

vectors = []
labels = []
for label, _ in sim_word:
    labels.append(label)
    vectors.append(embedding_model.wv[label])
print(vectors[0])
print(len(vectors[0]))
# sim_word는 ('단어',벡터값) 으로 되어있는 튜플 리스트야.
# labels에 유사단어 10개를 집어넣어
# 모델한테 단어를 주면, 그 단어의 100차원 벡터값을 줌. 10개 단어의 vector값을 vectors에 넣어
# vectors[0]을 프린트해보면 좌표 100개가 출력돼(100차원이니까 좌표도 100개)

df_vectors = pd.DataFrame(vectors)
print(df_vectors)
# 프린트해보면 df_vectors는  100개의 컬럼(0~99)에 각 차원의 좌표값들이 들어있어.
# sim_word 10개니까 vector값도 10개, 따라서 rows =  10

# 100차원을 시각화할 수 없으니 차원을 축소하자(2차원으로 줄이기ㅡ TSNE)
tsne_model = TSNE(perplexity=40, n_components=2,
                  init='pca', n_iter=2500, random_state=23)
new_value = tsne_model.fit_transform(df_vectors)
print(new_value)
print(type(new_value))
df_xy = pd.DataFrame({'words':labels,
                      'x':new_value[:, 0],
                      'y':new_value[:, 1]})
print(df_xy.tail(10))
print(df_xy.shape)
# TSNE는 차원축소해주는 모델(100차원 벡터를 2차원으로)
# 시작 지점을 랜덤으로 잡아, 근데 random_state=23 안주면 할 때마다 달라져
# 처음 값은 랜덤이지만, 할 때마다 같게끔 나오게돼.

# new value에는 2개의 벡터 값만 들어있어.
# 그걸 0번 인덱스를 x값으로, 1번 인덱스를 y값으로 하고 위에서 따놓은 label(유사단어 이름)
# 을 갖다가 데이터프레임을 만들어
# new_value는 슬라이싱으로 0번 인덱스를 전체 인덱싱 해주고 x에 주고
# 마찬가지로 슬라이싱으로 1번 인덱스를 전체인덱싱해서 y에 주었음.

# shape을 보면 (10,3)으로 나올 거야.

df_xy.loc[df_xy.shape[0]] = (key_word, 0,0)
print(df_xy.tail(11))


# 그래프에 현재 key_word는 없잖아. 그걸 0,0 좌표에다가 추가하겠다.
# df_xy.shape[0]은 shape의 앞 숫자.(row의 수) 예를들어 shape이 10,3이면
# 인덱스는 0~9이고, 인덱스 10번은 없지? 거기에 key_word를 0,0 좌표로 집어넣는 것

# 별 그리기
plt.figure(figsize=(8,8))  # 도화지 사이즈 정해주고
plt.scatter(0, 0, s=1500, marker='*')  # 한 가운데 별 그려준 것


for i in range(len(df_xy.x)-1):
    a = df_xy.loc[[i, len(df_xy.x) - 1], :]
    plt.plot(a.x, a.y, '-D', linewidth=2)
    plt.annotate(df_xy.words[i], xytext=(5,2),
                 xy=(df_xy.x[i], df_xy.y[i]),
                 textcoords='offset points',
                 ha = 'right', va = 'bottom')
plt.show()

# len(df_xy.x)는 11이지(위에 key_word 넣었으니까)
# i는 0~ 10까지가 되겠지(근데 마지막꺼 하나 안그어도 되니까 (키워드-키워드 그을 필요 없잖아)
# for문에서도 -1을 해주자. 그러면 뭔가를 10개 그리게 될 것이야.

# a는 리스트 안에 값이 두개야(i, len(df_xy.x)). 값을 두 개 뽑고, 컬럼은 다 뽑아내겠다.
# 그 아래 선을 그어. a의 x에는 0~9까지가 들어갈 것이고, y에는 키워드가 들어가.
# 걔네를 하나씩 선을 긋겠다.

# 10개중의 마지막 index=10번자료를 뽑아내겠다(여의도)
# 여의도까지 선을 쭉 긋겠다.
# plt.plot을 통해서 선을 10개를 긋게 되는 것이야.(선을 빼려면 주석처리하면됨)


# annotate는 그림에 주석다는 것.
# df_xy.words[i]: 각 좌표에 word가 한글로 출력
# offset points: 점 위에다 그리지 말고 조금 띄어라
# ha 수평정렬 va 수직정렬(영어면 baseline, 한글이니 bottom)
