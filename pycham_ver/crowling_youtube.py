## 유튜브에서 키워드 검색하기
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
## 크롤링
import os
import pandas as pd
import json
from pandas import json_normalize
import googleapiclient.discovery
import re

def get_image_title(url):
    # 웹 드라이버 초기화
    driver_path = "./webdriver/chromedriver.exe"

    # 크롬창 숨기는 옵션 추가
    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    driver = webdriver.Chrome(driver_path, options=options)
    driver.implicitly_wait(5) # or bigger second

    # 열고자 하는 채널
    driver.get(url)

    idx = 1
    url_idx = 1
    url_list = []
    video_url=[]

    while idx < 2:
        try:
            if idx % 1 == 0 :
                for i in range(2):
                    #스크롤 내리기
                    driver.execute_script('window.scrollBy(0, 1080);')
                    url_idx += 1
                    #각 동영상에 대한 url 가져오기(사진에 url이 있음)
                    img_url = driver.find_element_by_xpath(
                        '/html/body/ytd-app/div/ytd-page-manager/ytd-browse[1]/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[' + str(
                            url_idx) + ']/div[3]/ytd-video-renderer/div[1]/ytd-thumbnail/a/yt-img-shadow/img').get_attribute(
                        'src')
                    url_list.append(img_url)
                    time.sleep(2)

            idx += 1

        except Exception as e:
            print()
            print(e)
            break

    url_list = [v for v in url_list if v] #noun값이 있어서 url만 가져오기

    #전체 url에서 유튜브 url id 에 해당하는 부분만 가져오기
    for ks in url_list:
        a = ks.split('/')
        video_url.append(a[4])

    return video_url

keyword_swu = '거리두기' #키워드

#공식뉴스채널
news_channel = ["https://www.youtube.com/user/ytnnews24/search?query=", "https://www.youtube.com/c/MBCNEWS11/search?query=", "https://www.youtube.com/c/newskbs/search?query=", "https://www.youtube.com/sbs8news/search?query=", "https://www.youtube.com/user/JTBC10news/search?query="]
total_url_list = []

# ytn, mbc, kbs, sbs, jtbc 공식 뉴스채널에서 url가져오기
for eachURL in news_channel:
    url1 = eachURL+keyword_swu
    url2 = get_image_title(url1)
    for i in url2:
        total_url_list.append(i)

print("total url:", total_url_list) #특정 키워드를 검색한 영상들 비디오 id값 리스트




df = pd.DataFrame(columns=['command'])

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyDkhpDP9jaSlyCYSk3c-hGlYXQiY311LOA" #api 키

    URL = total_url_list #크롤링할 주소(위에서 자동 검색 결과 리스트)

    i = 0

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    for k in range(len(URL)):
        # print(URL[k])
        response = youtube.commentThreads().list(part='snippet,replies', videoId=URL[k], maxResults=100).execute()
        while response:
            for item in response['items']:
                i += 1
                comment = item['snippet']['topLevelComment']['snippet'] #대댓글을 말고 첫댓글만
                df.loc[i] = [comment['textDisplay']]
            if 'nextPageToken' in response:
                response = youtube.commentThreads().list(part='snippet,replies', videoId=URL[k],
                                                         pageToken=response['nextPageToken'], maxResults=100).execute()
            else:
                break


main()

#엑셀저장
df.to_excel('./data/댓글_youtube.xlsx')