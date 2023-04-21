import pandas as pd

data_scan = pd.read_csv('Nori_tool_address/data/data1.csv', encoding='cp949')
ini_scan = pd.read_csv('Nori_tool_address/ini_scans/ini1.csv')

# data_scan = {
#     'Tag_group' : ['L10_111', 'L10_222', 'L10_333', 'L10_444']
# }
# ini_scan = {
#     '태그 그룹' : ['L10_111', 'L10_222', 'L10_333']
# }
# df1 = pd.DataFrame(data_scan)
# df2 = pd.DataFrame(ini_scan)

data_scan['AD_FLAG'] = data_scan['Tag_group'].isin(ini_scan['태그 그룹']).map({True: 'OK', False: 'NO_TAG_GROUP'}) #map() 저게 왜 가능한 문법인지 모르겠음.. 좀 더 공부하자
if 'OK' in data_scan['AD_FLAG'].values: # 시리즈 형태의 컬럼 값을 if 문으로 비교할 때는 .values 를 사용한다 .values 공부하자
    # if ini_scan['start2'] <= data_scan['scan_buffer'] & ini_scan['end2'] >= data_scan['scan_buffer']:
    if ((ini_scan['start2'] <= data_scan['scan_buffer']) & (ini_scan['end2'] >= data_scan['scan_buffer'])).any(): #에러 해결 중...
        data_scan['PLC_AREA'] = ini_scan['레지스트 영역'].str.slice(0,2)
    else:
        data_scan['AD_FLAG'] = 'ERROR_SCAN_NO'





# result = []
# for i in df1.index:
#     for j in df2.index:
#         if df1.iloc[i][0] == df2.iloc[j][0]:
#             print(df1.iloc[i][0])
#             result.append(df1.iloc[i][0])
# result = df1[df1[0].isin(df2[0])][0].tolist() # df2의 첫 번째 열에 존재하는 값만 추출하여 리스트로 반환
# result = data_scan[data_scan['Tag_group'].isin(ini_scan['태그 그룹'])]['Tag_group'].tolist() # df2의 첫 번째 열에 존재하는 값만 추출하여 리스트로 반환











data_scan.to_csv('Nori_tool_address/Outputs/data.csv' #읽어들인 .txt 파일을 .csv 파일로 생성
           , encoding='utf-8-sig' 
           , index=False)

