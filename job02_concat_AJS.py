import pandas as pd

df = pd.read_csv('crawling_data/crawling_data_AJS/reviews_2018_1.csv')
# index 있으면 index_col=0 주면 됨
df.info()

# 연도별로 concat하는 코드
# 2018년도 concat

# # glob로 싹 가져와도 되는데, 여기서는 파일 이름이 정해져있으니 for문으로 가져오자
# df = pd.DataFrame()
# for i in range(1,51):
#     df_temp = pd.read_csv('./crawling_data/reviews_2018_{}.csv'.format(i))
#     df_temp.dropna(inplace=True)
#     df_temp.drop_duplicates(inplace=True)
#     df_temp.columns = ['title','reviews']
#     df_temp.to_csv('./crawling_data/reviews_2018_{}.csv'.format(i), index=False)
#     # 잘못된 데이터가 있을까봐 nan값, 중복값, 칼럼을 다시 제대로 준 것으로 덮어쓰는 것임.
#     df = pd.concat([df, df_temp], ignore_index=True)
#     # ignore_index=True 를 줘야 중복인덱스가 안생겨
# df.info()
# df.to_csv('./crawling_data/reviews_2018.csv', index=False)



# 전체년도 concat

df = pd.DataFrame()
for i in range(15,22):
    df_temp = pd.read_csv('./crawling_data/reviews_20{}.csv'.format(i))
    df_temp.dropna(inplace=True)
    df_temp.drop_duplicates(inplace=True)
    df_temp.columns = ['title','reviews']
    df_temp.to_csv('./crawling_data/reviews_20{}.csv'.format(i), index=False)
    df = pd.concat([df, df_temp], ignore_index=True)
df.drop_duplicates(inplace=True)
df.info()
df.to_csv('./crawling_data/naver_movie_reviews_2015_2021.csv', index=False)
