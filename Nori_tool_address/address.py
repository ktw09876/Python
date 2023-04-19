import pandas as pd

data = pd.read_csv('./Nori_tool_address/data/data1.csv', encoding='cp949')
ini_scan = pd.read_csv('./Nori_tool_address/ini_scans/ini1.csv')
print(ini_scan)

data['PLC_AREA'] = ini_scan['레지스트 영역'][0:3]

my_str[0:7]

# data.to_csv('Nori_tool_address/Outputs/data.csv' #읽어들인 .txt 파일을 .csv 파일로 생성
#            , encoding='utf-8-sig' 
#            , index=False)
