import requests
from bs4 import BeautifulSoup
import pyautogui


#검색어를 직접 입력
#keyword = input("검색어를 입력하세요>>>")
keyword = pyautogui.prompt("검색어를 입력하세요>>>")

lastpage = pyautogui.prompt("마지막 페이지번호를 입력해주세요")
pageNum = 1
for i in range(1, int(lastpage) * 10, 10): #range(시작, 끝, 단계), 입력 받은 정보는 str 형태기 때문에 형변환을 해줘야 함
    print(f"{pageNum}페이지 입니다+++")
    #naver 서버에 요청을 보냄, 검색어는 직접 입력 받음
    response = requests.get(f"https://search.naver.com/search.naver?where=news&sm=tab_jum&query={keyword}&start={i}")
    html = response.text

    #html 을 html.parser 로 번역한다
    soup = BeautifulSoup(html, 'html.parser')

    #'' 안에 css 선택자 인 대상 1개를 선택
    links = soup.select('.news_tit') #결과는 리스트 형태로 나온다

    #삼성전자 검색어 페이지 기사 10개의 제목과 링크를 가져온다
    for link in links:
        title = link.text #태그 안에 텍스트요소를 가져온다
        url = link.attrs['href'] #href 의 속성값을 가져온다
        print(title, url)
    pageNum = pageNum + 1
