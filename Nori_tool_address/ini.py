import pandas as pd

ini = pd.read_csv('./Nori_tool_address/ini/ini1.txt', sep = '\t') #구분자는 '\t' 로 지정

ini['start1'] = ini['레지스트 영역'].str.slice(3) #slice(인덱스번호, 인덱스번호) 두번째 인수가 없으면 끝까지

# print(ini['start1'])

start1 = pd.to_numeric(ini['start1']) #형변환 하려면? int() 대신 pd.to_numeric() 을 사용해야 한다
word_cnt = ini['워드 수']
ini['end1'] = start1 + word_cnt-1
ini['start2'] = ini['레지스트 영역2']
ini['end2'] = ini['start2'] + word_cnt-1



ini.to_csv('Nori_tool_address/ini_scans/ini1.csv' #읽어들인 .txt 파일을 .csv 파일로 생성
           , encoding='utf-8-sig' 
           , index=False) #인덱스는 생성하지 않겠다

