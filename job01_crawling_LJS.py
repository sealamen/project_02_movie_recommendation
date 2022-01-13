from selenium import webdriver
import pandas as pd  #폴더 옆에 RELOAD FROM DISK 누르면 갱신됌
from selenium.common.exceptions import NoSuchElementException
import time
# https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page=1
# //*[@id="old_content"]/ul/li[1]/a # 제목
# .click()
# //*[@id="movieEndTabMenu"]/li[6]/a
# //*[@id="movieEndTabMenu"]/li[6]/a  # 리뷰 버튼 누르기
# 총 리뷰 건수
# //*[@id="reviewTab"]/div/div/div[2]/span/em
# 첫번째 리뷰
# //*[@id="reviewTab"]/div/div/ul/li[1]/a/strong
# 리뷰 내용
# //*[@id="content"]/div[1]/div[4]/div[1]
# back()
# 리뷰 다 하나하나 크롤링 하고
# 리뷰페이지 2,3,4 .... 8,9, next
# //*[@id="pagerTagAnchor2"]
# //*[@id="pagerTagAnchor3"]/span
# //*[@id="pagerTagAnchor2"]/em  #다음으로

options= webdriver.ChromeOptions()
# options.add_argument('headless') #크롤링 하는 웹브라우저를 볼수가 없음
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')

driver = webdriver.Chrome('./chromedriver', options=options)




review_button_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a'
review_number_xpath = '//*[@id="reviewTab"]/div/div/div[2]/span/em'
try:
    for i in range(1, 38): #총 37페이지
        url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page={}'.format(i)
        titles = []
        reviews = []
        for j in range(1, 21):
            print(j+((i-1)*20), '번째 영화 크롤링 중')
            try:
                driver.get(url)
                movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(j) #영화 제목 따오기
                title = driver.find_element_by_xpath(movie_title_xpath).text

                driver.find_element_by_xpath(movie_title_xpath).click() # 영화제목 클릭
                review_page_url = driver.find_element_by_xpath(review_button_xpath).get_attribute('href') # 안에 주소를 긁어옴
                driver.get(review_page_url) #리뷰 링크로 들어가기
                # driver.find_element_by_xpath(review_button_xpath).click()
                # review_range = driver.find_element_by_xpath(review_number_xpath).text
                # review_range = review_range.replace(',', '')
                # review_range = int(review_range)
                # review_range = review_range // 10 +2
                review_range = int(driver.find_element_by_xpath(review_number_xpath).text.replace(',', '')) # 총 리뷰건수 예를들면 1,234->1234로 바꿔줌
                review_range = review_range // 10 + 2 # 한페이지당 리뷰 10개 잇으니깐
                if review_range > 6 : review_range = 5
                for k in range(1, review_range):

                    driver.get(review_page_url + '&page={}'.format(k)) # n번째 페이지를 가져와라
                    time.sleep(0.3)
                    for l in range(1, 11):
                        review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a/strong'.format(l)  # 첫번째 리뷰 제목 크롤링
                        try:
                            driver.find_element_by_xpath(review_title_xpath).click()  #첫번째 리뷰 제목 클릭
                            time.sleep(0.3)
                            review = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[4]/div[1]/div[4]').text #리뷰 내용 전부 크롤링
                            # print('================================= =================================')
                            # print(title)
                            # print(review)
                            titles.append(title)
                            reviews.append(review)
                            driver.back() # 뒤로가기
                        except:
                            # print(l, '번째 리뷰가 없다')
                            # driver.back()
                            # driver.back() #리뷰 끊기면 뒤로가기 두번해서 다시 다음 영화제목으로, 아니ㅣ면 다시 driver.get(url)
                            # driver.get(url)
                            break
            except:
                print('error')
        # try:
        #     for i in range(1, 38): .....
        # except:
        #     print('totally error')
        # finally:
        #     driver.close()

        df_review_20 = pd.DataFrame({'title':titles, 'reviews':reviews})
        df_review_20.to_csv('./crawling_data/reviews_{}_{}.csv'.format(2020, i), index=False)
except:
    print('totally error')
finally: #에러나든 안나든 모조건 실행
    driver.close()
# df_review = pd.DataFrame({'title':titles, 'reviews':'reviews'})
# df_review.to_csv('./crawling_data/reviews_{}.csv').format(2020)