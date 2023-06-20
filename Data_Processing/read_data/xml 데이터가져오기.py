import requests
from bs4 import BeautifulSoup

#구글의 자동완성 오픈API url
keyword = '스마트폰'
# url = 'http://suggestqueries.google.com/complete/search?output=toolbar&q=' + input()
url = 'http://suggestqueries.google.com/complete/search?output=toolbar&q=' + keyword

#get요청을 보낸 후 변수에 담음
response = requests.get(url)

#BeautifulSoup()로 API 분석, 파싱 '.content', '.text'둘 다 가능
# soup = BeautifulSoup(response.content, 'xml')
soup = BeautifulSoup(response.text, 'xml')
print(soup)

#'suggestion'태그를 찾고
datas1 = soup.select('suggestion')

for item in datas1:
    #'data'속성값을 출력
    print(item['data'])