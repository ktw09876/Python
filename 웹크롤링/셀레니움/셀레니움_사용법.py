from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

#크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

#브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

#불필요한 에러메시지 없애기
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

#웹 브라우저 띄우기
service = Service(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)

browser.maximize_window() #화면 최대화
browser.get("https://www.naver.com")
browser.implicitly_wait(10) #로딩이 끝날때까지 10를 기다림

#쇼핑 매뉴 클릭
browser.find_element(By.CSS_SELECTOR, 'a> .type_shopping').click()
time.sleep(5) # 쇼핑 배너를 클릭한 뒤, 아직 페이지가 뜨지도 않았는데 바로 다음 명령어가 실행될 수도 있으니까, 2초 정도 여유를 준다.

#검색창 클릭 
search = browser.find_element(By.CSS_SELECTOR, 
    '#__next > div > div.pcHeader_header__tXOY4 > div > div > div._gnb_header_area_150KE > div > div._gnbLogo_gnb_logo_3eIAf > div > div._gnbSearch_gnb_search_3O1L2 > form > div._gnbSearch_inner_2Zksb > div > input'
                              ).click() #적용 안됨 원인 찾아보기


# #검색어 입력
search.send_keys('아이폰 13')
search.send_keys(Keys.ENTER)
