import requests
from bs4 import BeautifulSoup

#example1
#naver 서버에 요청을 보냄, 검색어 '삼성전자'
response = requests.get("https://search.naver.com/search.naver?where=news&sm=tab_jum&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90")
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

#example2
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'} #내가 접속한 브라우저 정보를 알려줌, 로봇이 아닌 사람이 접근했다고 알리는 기능
url = 'https://www.transfermarkt.com/'
r = requests.get(url, headers=headers) 
#print(r.status_code)했을때 200 이 나와야 정상적으로 요청이 처리됨
#print(r.status_code) 

#공식문서 Quick Start
html_doc = """<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>"""

soup = BeautifulSoup(html_doc, 'html.parser')
# soup = BeautifulSoup(r.text, 'html.parser')

# #p 태그 정보 가져오기
# a_list = soup.find_all('a')
# for i in a_list:
#     print(i.text)

print(soup.find_all('a', {'id':'link3'}))
