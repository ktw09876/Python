import pandas as pd

data = pd.read_csv('./Address/data/data1.csv', encoding='cp949')
ini_scan = pd.read_csv('./Address/ini_scans/ini1.csv')
print(ini_scan)

data['PLC_AREA'] = ini_scan['레지스트 영역'][0:3]

my_str[0:7]
