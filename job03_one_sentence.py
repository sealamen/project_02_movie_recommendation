import pandas as pd

df = pd.read_csv('./crawling_data/naver_movie_reviews_2015_2021.csv')
# print(df)
# print(df['title'])
# print(df['title'].unique())
# print(type(df['title'].unique()))
# exit()

one_sentences = []
for title in df['title'].unique():
    temp = df[df['title'] == title]
    temp = temp['reviews']
    one_sentence = ' '.join(temp)
    one_sentences.append(one_sentence)

    # df['title']하면 title 컬럼만 있는 시리즈형태. 제목만 뽑아온 데이터프레임인것.
    # 거기서 .unique() 하면 중복 없이 제목이 하나씩 있는 ndarray 형태.
    # for문을 통해 제목을 하나씩 따와서 title을 하나씩 뽑아올거야.
    # 거기서 title이 for문의 title인 애들만 다 뽑아온 데이터프레임이 temp
    # 그 temp에서 리뷰들만 따온 것을 다시 temp에 넣어주자

    # 문자열 합치는 join 함수를 통해 한 문장으로 합쳐줄 것이 one_sentence
    # 그러면 각 영화별로 리뷰가 한 문장으로 묶여서 들어갈 것. 이걸 빈 리스트(one_sentences)에 넣자
    # 이걸 가지고 다시 데이터프레임을 만들 것이야.

    # 예를들어 title이 기생충이야.
    # 기생충을 하나 가져와서 기생충이라는 이름으로 제목을 검색을 해.
    # 그럼 거기에 리뷰들을 다 뽑아와서 하나의 문장으로 join 해준다.

df_one_sentences = pd.DataFrame(
    {'titles':df['title'].unique(), 'reviews':one_sentences})
    # 기생충, 강철비가 그대로 들어갈 것이고, one_sentences
print(df_one_sentences)
df_one_sentences.to_csv('./crawling_data/naver_movie_reviews_onesentence_2015_2021.csv', index=False)
