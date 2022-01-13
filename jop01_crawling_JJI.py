from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time


options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('lang=ko_KR')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-gpu')
driver = webdriver.Chrome('./chromedriver', options=options)
pages = [37]
# 40,35,40,45,50,55,70,75,60,40,40,25,20,25,25,20,20,35,15,15,15,15
year = 2020

try:
    for page in pages:
        titles = []
        reviews = []
        for i in range(1, page):
            url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={}&page={}'.format(year, i)
            for j in range(1, 21):
                try:
                    driver.get(url)
                    title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(j)
                    title = driver.find_element_by_xpath(title_xpath).text
                    driver.find_element_by_xpath(title_xpath).click()
                    print(title, '크롤링 중')

                    review_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a'
                    review_page_url = driver.find_element_by_xpath(review_xpath).get_attribute('href')
                    driver.get(review_page_url)
                    review_range = driver.find_element_by_xpath('//*[@id="reviewTab"]/div/div/div[2]/span/em').text
                    review_range = int(review_range.replace(',', '')) // 10 + 2
                    if review_range > 6:
                        review_range = 6
                    for k in range(1, review_range):
                        driver.get(review_page_url + '&page={}'.format(k))
                        # review_page_xpath = '//*[@id="pagerTagAnchor{}"]'.format(k)
                        # driver.find_element_by_xpath(review_page_xpath).click()
                        for l in range(1, 11):
                            review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a/strong'.format(l)
                            try:
                                driver.find_element_by_xpath(review_title_xpath).click()
                                review = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[4]/div[1]/div[4]').text
                                reviews.append(review)
                                titles.append(title)
                                driver.back()
                            except:
                                break
                        print(len(titles), len(reviews))
                except:
                    print('error')
            df_review_20 = pd.DataFrame({'title': titles, 'reviews': reviews})
            df_review_20.to_csv('./crawling_data/reviews_{}_{}.csv'.format(year, i), index=False)
            titles = []
            reviews = []
        # df_review = pd.DataFrame({'title': titles, 'reviews': reviews})
        # df_review.to_csv('./crawling_data/reviews_{}.csv'.format(year), index=False)
        # year = year - 1
except:
    print('totally error')
finally:
    driver.close()
