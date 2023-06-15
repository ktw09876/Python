import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

#내가 접속한 브라우저 정보를 알려줌, 로봇이 아닌 사람이 접근했다고 알리는 기능
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'} 

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
    # print(len(player_info))

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

time.sleep(1)

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
# #df.info(), df.shape로 데이터 파악
# print(df.info())

#.csv파일로 저장
df.to_csv('transfermarkt50.csv', index = False, encoding='utf-8-sig' )

# #'age'를 조건으로 데이터를 가져오고싶은데 type이 object라서 비교할 수 없음 --> int형으로 변환
# df_int = df.astype({'age':'int' })

# #'age'이 30이상인 대상의 'name', 'value'를 가져온다
# result = df_int.loc[df_int['age'] >= 30, ['name', 'value'] ]
# print(result)

#'value'에 13을 곱해서 '시장가치(억)'컬럼을 만들자
#'value'의 특수문자 제거
df['value'] = df['value'].str.replace('€', '')
df['value'] = df['value'].str.replace('m', '').astype('float') #특수문자 제거 후 타입을 int로
# print(df['value'])

#'사장가치(억)'컬럼 생성
df['시장가치(억)'] = df['value'] * 13
# print(df)

#'value'컬럼 삭제
df = df.drop(columns=['value'])
print(df)

#.csv파일로 저장
df.to_csv('transfermarkt50.csv', index = False, encoding='utf-8-sig' )

