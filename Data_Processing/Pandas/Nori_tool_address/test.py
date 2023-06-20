import pandas as pd
import cx_Oracle

# # 원본 data의 행 개수가 늘어났을 때 .apply() 를 이용한 좀 더 효율적인 방법

#함수정의
# def check_tag_group(row, ini_scan):
#     if row['Tag_group'] in ini_scan.loc[:, '태그 그룹'].values:
#         ini_scan_row = ini_scan[ini_scan['태그 그룹'] == row['Tag_group']].iloc[0]
#         if int(row['scan_buffer']) >= int(ini_scan_row['start2']) and int(row['scan_buffer']) <= int(ini_scan_row['end2']):
#             if ini_scan_row['off_set'] == 1:
#                 row['AD_FLAG'] = 'ERROR_OFFSET'
#             else:
#                 row['AD_FLAG'] = 'OK'
#                 row['PLC_AREA'] = ini_scan_row['레지스트 영역'][:3]
#                 if int(ini_scan_row['레지스트 영역'][-5:]) > int(ini_scan_row['레지스트 영역2']):
#                     row['cal_scan_buffer'] = int(row['scan_buffer']) + (int(ini_scan_row['레지스트 영역'][-5:]) - int(ini_scan_row['레지스트 영역2']))
#                 elif int(ini_scan_row['레지스트 영역'][-5:]) < int(ini_scan_row['레지스트 영역2']):
#                     row['cal_scan_buffer'] = int(row['scan_buffer']) - (int(ini_scan_row['레지스트 영역2']) - int(ini_scan_row['레지스트 영역'][-5:]))
#                 else:
#                     row['cal_scan_buffer'] = row['scan_buffer']
#                 if pd.isna(row['비트']):
#                     row['FULL_ADDRESS'] = ini_scan_row['레지스트 영역'][:3] + str(row['cal_scan_buffer']).rjust(5,'0')
#                 else:
#                     row['FULL_ADDRESS'] = ini_scan_row['레지스트 영역'][:3] + str(row['cal_scan_buffer']).rjust(5,'0') + '.' + str(int(row['비트'])).rjust(2, '0')
#         else:
#             row['AD_FLAG'] = 'ERROR_SCAN_NO'
#     else:
#         row['AD_FLAG'] = 'NO_TAG_GROUP'
#     return row

# data_scan = data_scan.apply(check_tag_group, axis=1, args=(ini_scan,))



