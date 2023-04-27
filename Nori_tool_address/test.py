# import pandas as pd

# data_scan = pd.read_csv('Nori_tool_address/data/data1.csv', encoding='cp949')
# ini_scan = pd.read_csv('Nori_tool_address/ini_scans/ini1.csv')

# # 원본 data의 행 개수가 늘어났을 때 .apply() 를 이용한 좀 더 효율적인 방법
# # # 함수 정의
# def calculate_full_address(data_scan_row):
#     AD_FLAG = ''
#     PLC_AREA = ''
#     FULL_ADDRESS = ''
#     cal_scan_buffer = ''

#     if data_scan_row['Tag_group'] in ini_scan['태그 그룹'].values:
#         ini_scan_row = ini_scan[ini_scan['태그 그룹'] == data_scan_row['Tag_group']]
#         ini_scan_row = ini_scan_row.squeeze()

#         if int(data_scan_row['scan_buffer']) >= int(ini_scan_row['start2']) and int(data_scan_row['scan_buffer']) <= int(ini_scan_row['end2']):
#             AD_FLAG = 'OK'
#             PLC_AREA = ini_scan_row['레지스트 영역'][:3]

#             if int(ini_scan_row['레지스트 영역'][-5:]) > int(ini_scan_row['레지스트 영역2']):
#                 cal_scan_buffer = int(data_scan_row['scan_buffer']) + (int(ini_scan_row['레지스트 영역'][-5:]) - int(ini_scan_row['레지스트 영역2']))
#             elif int(ini_scan_row['레지스트 영역'][-5:]) < int(ini_scan_row['레지스트 영역2']):
#                 cal_scan_buffer = int(data_scan_row['scan_buffer']) - (int(ini_scan_row['레지스트 영역2']) - int(ini_scan_row['레지스트 영역'][-5:]))
#             else:
#                 cal_scan_buffer = data_scan_row['scan_buffer']

#             FULL_ADDRESS = PLC_AREA + str(cal_scan_buffer).rjust(5,'0')

#             if not pd.isna(data_scan_row['비트']):
#                 FULL_ADDRESS += '.' + str(int(data_scan_row['비트'])).rjust(2, '0')
#         else:
#             AD_FLAG = 'ERROR_SCAN_NO'
#     else:
#         AD_FLAG = 'NO_TAG_GROUP'

#     return pd.Series([AD_FLAG, PLC_AREA, FULL_ADDRESS, cal_scan_buffer])

# # # apply()를 사용하여 함수 적용
# data_scan[['AD_FLAG', 'PLC_AREA', 'FULL_ADDRESS', 'cal_scan_buffer']] = data_scan.apply(calculate_full_address, axis=1)



