import requests
from bs4 import BeautifulSoup

url = 'https://www.lottecinema.co.kr/NLCHS/Cinema/Detail?divisionCode=1&detailDivisionCode=1&cinemaID=1009'
html = requests.get(url)

soup = BeautifulSoup(html.text, 'html.parser')
print(soup)
# title_list = soup.seelect('#timeTable > div.mCustomScrollbar.timeScroll > div:nth-child(1) > div')
# title_list = soup.select_one('#contents > div.theater_top_wrap > div.info_wrap > dl.theater_notice > dd > a')
# print(title_list)