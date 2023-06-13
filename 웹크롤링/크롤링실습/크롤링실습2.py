import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'} #내가 접속한 브라우저 정보를 알려줌, 로봇이 아닌 사람이 접근했다고 알리는 기능

#선수의 정보를 담을 리스트
number = []
name = []
position = []
age = []
nation = []
team = []
value = []

for i in range(1,3):

    url = f'https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop?utm_source=Instagram&utm_medium=Insta_bio&utm_campaign=Insta_bio_most_valuable_players&page={i}'
    html = requests.get(url, headers=headers)
    #print(r.status_code)했을때 200 이 나와야 정상적으로 요청이 처리됨
    # print(r.status_code) 

    #BeautifulSoup()로 웹페이지 분석
    soup = BeautifulSoup(html.text, 'html.parser')

    #tr태그이면서 class가 'odd', 'even'인 대상, 리스트 형태임
    player_info = soup.find_all('tr', class_ = ['odd', 'even'])
    print(len(player_info))

    #player_info에서 'td'태그만 모두 찾기
    for info in player_info:
        td = info.find_all('td')
        # print(td)

        #찾은 정보를 각리스트에 추가, .append()
        number.append(td[0].text)
        name.append(td[3].text)
        position.append(td[4].text)
        age.append(td[5].text)
        nation.append(td[6].img['alt'])
        team.append(td[7].img['alt'])
        value.append(td[8].text)

time.sleep(2)

#각 리스트들을 데이터프레임으로
df = pd.DataFrame(
    {
          'number': number
        , 'name': name
        , 'position': position
        , 'age': age
        , 'nation': nation
        , 'team': team
        , 'value': value
    }
)
print(df)

#.csv파일로 저장
df.to_csv('transfermarkt50.csv', index=False)
