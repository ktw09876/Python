import pandas as pd

ini = pd.read_csv('./Address/ini/ini1.txt', sep = '\t') #구분자는 '\t' 로 지정
df = pd.DataFrame(ini) ## 데이터프래임 생성

df['start1'] = ini['레지스트 영역'].str.slice(3) #slice(인덱스번호, 인덱스번호) 두번째 인수가 없으면 끝까지
word_cnt = ini['워드 수']
start1 = pd.to_numeric(df['start1']) #형변환 하려면? int() 대신 pd.to_numeric() 을 사용해야 한다
df['end1'] = start1 + word_cnt-1
df['start2'] = start1 + word_cnt
start2 = df['start2']
df['end2'] = start2 + word_cnt-1



ini.to_csv('Address/ini_scans/ini1.csv' #읽어들인 .txt 파일을 .csv 파일로 생성
           , encoding='utf-8-sig' 
           , index=False) #인덱스는 생성하지 않겠다

