import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QStringListModel  # 자동완성을 위해 필요
from PyQt5 import uic   # ui를 클래스로 바꿔준다
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from gensim.models import Word2Vec
from scipy.io import mmread
import pickle

form_window = uic.loadUiType('./movie_recommendation.ui')[0]
class Exam(QWidget, form_window):
    def __init__(self):   # 버튼 누르는 함수 처리해주는 곳
        super().__init__()
        self.setupUi(self)
        self.df_reviews = pd.read_csv('./crawling_data/cleaned_review_2015_2021.csv')
        self.Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
        self.embedding_model = Word2Vec.load('./models/word2VedModel_2015_2021.model')
        with open('./models/tfidf.pickle', 'rb') as f:
            self.Tfidf = pickle.load(f)
        # 자료 가져오고 하는 것은 처음 시작할 때(init 안에서) 다 하면 되겠지.

        # 콤보 박스에 목록을 넣어주는 부분
        self.titles = list(self.df_reviews['titles'])
        self.titles.sort()
        for title in self.titles:
            self.cmb_titles.addItem(title)
        # addItem하면 콤보박스에 목록을 넣어줘
        # for문을 돌리면 다 들어가겠지


        # 자동완성기능
        model = QStringListModel()
        model.setStringList(self.titles)
        completer = QCompleter()
        completer.setModel(model)
        self.le_keyword.setCompleter(completer)
        # QCompleter 는 일반적으로 QLineEdit 또는 QComboBox 와 함께 사용

        self.cmb_titles.currentIndexChanged.connect(self.cmb_titles_slot)
        self.btn_recommend.clicked.connect(self.btn_recommend_slot)
        # 버튼 누르면 추천이 진행되게끔

    #콤보박스 함수
    def cmb_titles_slot(self):
        title = self.cmb_titles.currentText()
        recommendation_titles = self.recommend_by_movie_title(title)
        self.lbl_recommend.setText(recommendation_titles)


        # 콤보박스에서 선택됐을 경우에서의 출력

    # 영화 추천해주는 함수(08에서 따왔음, 함수 안에서 선언했으니 self 붙여주자)
    def getRecommendation(self, cosine_sim):
        simScore = list(enumerate(cosine_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1],
                          reverse=True)
        simScore = simScore[1:11]  # 내림차순으로 나올테니 가장 처음에 나오는 것은 자기자신. 그러므로 처음은 제외
        movieidx = [i[0] for i in simScore]
        recMovieList = self.df_reviews.iloc[movieidx]
        return recMovieList.titles   # ['titles'] 해도 됨
        # df_reviews는 self 안에서 불러온 것이니 self 변수. 앞에 self 붙여주자
        # 타이틀들만 리턴해주면 되겠지

    def btn_recommend_slot(self):
        key_word = self.le_keyword.text() # 키워드는 label editor로 받는 글자
        if key_word:
            if key_word in self.titles:   # 만약에 완전히 같은 문자열이라면 영화타이틀로 본다
                recommendation_titles = self.recommend_by_movie_title(key_word)
                self.lbl_recommend.setText(recommendation_titles)
                # 키워드(영화 제목인 경우)를 넣었을 경우의 출력
            else:     # 키워드가 아니면 첫 번째 단어만 보겠다
                key_word = key_word.split()
                if len(key_word) > 20:
                    key_word = key_word[:20]
                # 띄어쓰기를 기준으로 키워드를 자르고 리스트로 받자
                # 아래서 key_word의 [0] 번만 뽑아줘
                # 그래서 '겨울 왕국'이면 겨울만 받도록
                # 키워드가 20자 이상이면 20자만 받자

                if len(key_word) > 10:
                    sentence = ' '.join(key_word)
                    recommendation_titles = self.recommend_by_sentence(sentence)
                    self.lbl_recommend.setText(recommendation_titles)
                else:
                    sentence = [key_word[0]] * 11
                    try:
                        sim_word = self.embedding_model.wv.most_similar(key_word[0], topn=10)
                    except:
                        self.lbl_recommend.setText('제가 모르는 단어에요 ㅠㅠ')
                        return  # 죽지 않으려면 return해서  sim_word를 종료해버려야해
                    words = []
                    for word, _ in sim_word:
                        words.append(word)
                    for i, word in enumerate(words):
                        sentence += [word] * (10 - i) # 가장 유사한 애는 10번, 그 다음은 9번...
                    sentence = ' '.join(sentence)
                    recommendation_titles = self.recommend_by_sentence(sentence)
                    self.lbl_recommend.setText(recommendation_titles)
                    # 키워드(영화 제목이 아닌 경우)를 넣었을 경우의 출력


    # 아래있는 애들은 중복되는거 함수로 바꿔준 것

    def recommend_by_sentence(self, sentence):
        sentence_vec = self.Tfidf.transform([sentence])
        cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)
        recommendation_titles = self.getRecommendation(cosine_sim)
        recommendation_titles = '\n'.join(list(recommendation_titles))
        return recommendation_titles

    def recommend_by_movie_title(self, title):
        movie_idx = self.df_reviews[self.df_reviews['titles'] == title].index[0]  # 해당 영화제목의 위치를 받음
        cosine_sim = linear_kernel(self.Tfidf_matrix[movie_idx],
                                   self.Tfidf_matrix)
        recommendation_titles = self.getRecommendation(cosine_sim)
        recommendation_titles = '\n'.join(list(recommendation_titles))
        return recommendation_titles

        # 문장을 tfidf 모델에 줘버리면 문장의 벡터값이 나와
        # linear_kernel에 벡터값과 매트릭스를 주면 코사인유사도를 계산해줘
        # 그 코사인 값을 기준으로 10개를 추천해주고
        # 시리즈로는 setText 안되니까 문자열로 바꾸자.
        # 시리즈를 리스트로 바꾼다음에 그걸 줄바꿈으로 이어붙이면 10줄(영화제목 10개)이 되겠지

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())

