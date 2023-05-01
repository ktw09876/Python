# import pandas as pd


# data_scan = pd.DataFrame({
#     'Tag_group':[
#         'L10_111','L10_111','L10_111','L10_111','L10_111','L10_222','L10_222','L10_222','L10_222','L10_333','L10_333','L10_333','L10_333','L10_333','L10_444','L10_444'
#     ],
#     'Tag_name': [
#         None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None
#     ],
#     'scan_buffer':[
#         '10','100','1000','2000','4000','18000','19000','20000','22000','6000','7000','8000','9000','10000','1000','2000'
#     ],
#     '비트':[
#         None,None,None,None,None,'0','1','2','3','4','5',None,None,None,None,None
#     ]
# })
# ini_scan = pd.DataFrame({
#     '레지스트 영역':[
#         'EM000000','EM000900','EM001800','EM002700','DM003600','DM004500','DM005400','DM116300','DM117200','DM118100'
#     ],
#     '워드 수':[
#         '900','900','900','900','900','900','900','900','900','900'
#     ],
#     '태그 그룹':[
#         'L10_111','L10_111','L10_111','L10_111','L10_222','L10_222','L10_222','L10_333','L10_333','L10_333'
#     ],
#     '레지스트 영역2':[
#         '0','900','1800','2700','18600','19500','20400','6300','7200','8100',
#     ],
#     'start2':[
#         '0','900','1800','2700','18600','19500','20400','6300','7200','8100'
#     ],
#     'end2':[
#         '899','1799','2699','3599','19499','20399','21299','7199','8099','8999'
#     ],
#     'off_set':[
#     '0','0','0','0','0','0','0','0','0','0'
#     ]
# })

# #.txt 파일이 두 개 이상 경우
# data_path = 'Nori_tool_address/data/'
# data_list = [
#         'data1.csv',
#         'data2.csv'
#     ]

# #데이터프레임 생성, '라인 구분' 컬럼 추가
# data_dfs = []
# for data_name in data_list:
#     df = pd.read_csv(data_path + data_name, encoding='cp949')
#     df['라인 구분'] = df['Tag_group'].str.slice(0,3)
#     data_dfs.append(df)


# data_scan = pd.concat(data_dfs, ignore_index=True) #읽어들인 데이터프레임을 하나로 합친다
# ini_scan = pd.read_csv('Nori_tool_address/ini_scans/ini1.csv')
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



