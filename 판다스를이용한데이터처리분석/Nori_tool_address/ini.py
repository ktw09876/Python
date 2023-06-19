import os
import pandas as pd

#.txt 파일이 한 개의 경우
# ini = pd.read_csv('Nori_tool_address/ini/ini1.txt', sep = '\t') #구분자는 '\t' 로 지정

#.txt 파일이 두 개 이상 경우
ini_path = 'Nori_tool_address/ini/'
ini_list = [
        'ini1.txt',
        'ini2.txt'
    ]

#필요한 컬럼 생성
ini_dfs = []
for ini_name in ini_list:
    df = pd.read_csv(ini_path + ini_name, delimiter="\t")
    df.insert(0, '파일명', "") #'파일명' 컬럼을 인덱스 0 번째에 생성
    df['파일명'] = os.path.basename(ini_name)
    ini_dfs.append(df)

ini = pd.concat(ini_dfs, ignore_index=True) 

ini['start1'] = ini['레지스트 영역'].str.slice(3).astype(int) #slice(인덱스번호, 인덱스번호) 두번째 인수가 없으면 끝까지
ini['end1'] = ini['레지스트 영역'].str.slice(3).astype(int) + (ini['워드 수'].astype(int)-1)
ini['start2'] = ini['레지스트 영역2']
ini['end2'] = ini['start2'].astype(int) + (ini['워드 수'].astype(int)-1)

#'레지스트 영역' 컬럼에 ';' 가 포함된 경우 주석 --> 사용하지 않는 범위임
ini['off_set'] = ini['레지스트 영역'].apply(lambda x: 1 if ';' in x else 0) #apply(), lambda 좀 더 공부하자



ini.to_csv('Nori_tool_address/ini_scans/ini1.csv' #읽어들인 .txt 파일을 .csv 파일로 생성
           , encoding='utf-8-sig' 
           , index=False) #인덱스는 생성하지 않겠다
