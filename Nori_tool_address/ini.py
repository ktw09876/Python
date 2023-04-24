import pandas as pd

ini = pd.read_csv('./Nori_tool_address/ini/ini1.txt', sep = '\t') #구분자는 '\t' 로 지정


ini['start1'] = ini['레지스트 영역'].str.slice(3).astype(int) #slice(인덱스번호, 인덱스번호) 두번째 인수가 없으면 끝까지
ini['end1'] = ini['레지스트 영역'].str.slice(3).astype(int) + (ini['워드 수'].astype(int)-1)

#if 문을 사용하려면 조건 모두 True or False 이어야 하기때문에 반복문을 사용해야 한다
# for i, ini_row in ini.iterrows():
#     if int(ini.at[i, '레지스트 영역'][-5:]) > int(ini.at[i, '레지스트 영역2']):
#         ini.at[i, 'start2'] = int(ini.at[i, '레지스트 영역'][-5:])
#     else:
#         ini.at[i, 'start2'] = ini.at[i, '레지스트 영역2']

ini['start2'] = ini['레지스트 영역2']
ini['end2'] = ini['start2'].astype(int) + (ini['워드 수'].astype(int)-1)




ini.to_csv('Nori_tool_address/ini_scans/ini1.csv' #읽어들인 .txt 파일을 .csv 파일로 생성
           , encoding='utf-8-sig' 
           , index=False) #인덱스는 생성하지 않겠다
