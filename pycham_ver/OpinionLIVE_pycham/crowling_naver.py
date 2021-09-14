import requests
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium import webdriver
import time
import re
import pandas as pd

# 변수 설정
QUERY = '백신접종 "경제회복"' ####input
serach_query = urllib.parse.urlencode({'query': QUERY}, encoding='utf-8')
URL = f"https://search.naver.com/search.naver?where=news&sm=tab_pge&{serach_query}\
    &sort=0&photo=0&field=0&pd=0&ds=&de=&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all"

link_pattern = "https://news.naver.com/main/read.naver?"
search_PAGE = 10

# driver 설정
# 크롬창 숨기는 옵션 추가
options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(executable_path="webdriver\chromedriver.exe", options=options)



# 검색 결과 내 링크 찾기 : news.naver.come으로 시작하는 모든 링크 반환
def get_news_links(page_num, link_pattern):
    links = []
    links_number = 0
    for page in range(page_num):
        print(f"Scrapping page : {page + 1}")
        req = requests.get(f"{URL}&start={10 * page + 1}");
        soup = BeautifulSoup(req.text, 'lxml')
        results = soup.find_all('a', {'href': re.compile(link_pattern)})
        for result in results:
            links.append(result['href'])
            links_number = links_number +1
            if links_number > 150:
                break

    print(f"총 {len(links)}개의 뉴스를 찾았습니다.")  # 확인용
    return links


# 한 페이지 별로 필요한 정보 스크레이핑
def extract_info(url, wait_time=1, delay_time=0.3):
    driver.implicitly_wait(wait_time)
    driver.get(url)

    # 댓글 창 있으면 다 '더보기' 클릭
    while True:
        try:
            more_comments = driver.find_element_by_css_selector('u_cbox_in_view_comment')
            more_comments.click()
            time.sleep(delay_time)

        except:
            break

    # html 페이지 읽어오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    try:

        # 댓글 내용
        contents = soup.find_all("span", {"class": "u_cbox_contents"})
        contents = [content.text for content in contents]
        # 취합
        reply_number = 0
        for i in contents:
            results_test.append(i)
            reply_number = reply_number + 1
            print(i)
            print("------")

        print("완료")
        return results_test

    except:
        print("오류")


# 각 페이지 돌면서 스크래핑
def extract_contents(links):
    Contents = []
    for link in links:
        Content = extract_info(f"{link}&m_view=1")  # 각각의 링크에 대해 extract_info 호출
        Contents.append(Content)  # extract_info의 결과로 나오는 dic 저장
    return Contents


# 모든 작업 진행
def main():
    global search_PAGE
    news_links = get_news_links(search_PAGE, link_pattern)
    result = extract_contents(news_links)
    driver.quit()
    return result
    print(result[0])


results_test = []
main()
results_df = pd.DataFrame(results_test)
results_df.columns = ['command']
results_df.to_excel('./data/댓글_naver.xlsx',encoding='utf-8-sig')