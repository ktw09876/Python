import pandas as pd

data_scan = pd.read_csv('./Nori_tool_address/data/data1.csv', encoding='cp949')
ini_scan = pd.read_csv('./Nori_tool_address/ini_scans/ini1.csv')
df = pd.DataFrame({
        'data_tag_group' : data_scan['Tag_group'],
        'ini_tag_group' : ini_scan['태그 그룹'],
        'scan_buffer' : data_scan['scan_buffer'],
        'start2' : ini_scan['start2'], 
        'end2' : ini_scan['end2']
    })

# data['PLC_AREA'] = ini_scan['레지스트 영역'].str.slice(0,3) #PLC_AREA 로직

#PLC_AREA 로직 추가
# scan_buffer = pd.to_numeric(df['scan_buffer'])
print(df)


# if (df.data_tag_group == df.ini_tag_group):
#     if df.scan_buffer >= df.start2 & df.scan_buffer <= df.start2:
#         data_scan['AD_FLAG'] = 'OK'
#         data_scan['PLC_AREA'] = ini_scan['레지스트 영역'].str.slice(0,3)
#     else:
#         data_scan['PLC_AREA'] = '확인 필요'
# else:
#     data_scan['AD_FLAG'] = 'ERROR_SCAN_NO'

# print(df.data_tag_group == df.ini_tag_group)

# df_data.to_csv('Nori_tool_address/Outputs/data.csv' #읽어들인 .txt 파일을 .csv 파일로 생성
#            , encoding='utf-8-sig' 
#            , index=False)

