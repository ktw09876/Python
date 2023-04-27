import pandas as pd
import numpy as np

#.csv 파일이 한 개 경우
# data_scan = pd.read_csv('Nori_tool_address/data/data1.csv', encoding='cp949')

#.txt 파일이 두 개 이상 경우
data_path = 'Nori_tool_address/data/'
data_list = [
        'data1.csv',
        'data2.csv'
    ]

#데이터프레임 생성, '라인 구분' 컬럼 추가
data_dfs = []
for data_name in data_list:
    df = pd.read_csv(data_path + data_name, encoding='cp949')
    df['라인 구분'] = df['Tag_group'].str.slice(0,3)
    data_dfs.append(df)


data_scan = pd.concat(data_dfs, ignore_index=True) #읽어들인 데이터프레임을 하나로 합친다
ini_scan = pd.read_csv('Nori_tool_address/ini_scans/ini1.csv')


#같은 로직을 사용자 정의 함수를 이용해서 처리
def address(data_scan):
    #컬럼 추가
    # data_scan.insert(4, 'cal_scan_buffer', "")
    # data_scan.insert(5, 'AD_FLAG', "")
    # data_scan.insert(6, 'PLC_AREA', "")
    # data_scan.insert(7, 'FULL_ADDRESS', "")
    data_scan['cal_scan_buffer'] = ""
    data_scan['AD_FLAG'] = ""
    data_scan['PLC_AREA'] = ""
    data_scan['FULL_ADDRESS'] = ""

    #'Tag_group' 의 값이 '태그 그룹' 에 있는지 검사
    if data_scan['Tag_group'] in ini_scan['태그 그룹'].values: #1개 행마다 값을 비교하기 때문에 row[] 를 사용, loc[인덱스, 컬럼명], : 는 모든 행 선택
        #'Tag_group' 의 값이 '태그 그룹' 에 있으면서 'scan_buffer' 값이 'start2', 'end2' 범위에 들어오는 경우
        if data_scan['Tag_group'] == ini_scan['태그 그룹'].values and int(data_scan['scan_buffer']) >= int(ini_scan['start2']) & int(data_scan['scan_buffer']) <= int(ini_scan['end2']): 
            #.txt 파일에서 주석처리 부분                                
            if ini_scan['off_set'] == 1:
                data_scan['AD_FLAG'] = 'ERROR_OFFSET'
            else:        
                data_scan['AD_FLAG'] = 'OK' #'Tag_group' 의 값이 '태그 그룹' 에 있는 data_scan 의 i 번째 행의 'AD_FLAG' 컬럼에 'OK'
                data_scan['PLC_AREA'] = ini_scan['레지스트 영역'][:3]# 'PLC_AREA' 컬럼에 레지스트 영역의 왼쪽부터 3자리 입력, ini_scan 은 ['레지스트 영역'] 컬럼 전체를 가져오기 때문에 ini_scan_row 를 사용한다, 
                #'레지스트 영역' 뒤 부터 5자리가 '레지스트 영역2' 보다 큰 경우
                if int(ini_scan['레지스트 영역'][-5:]) > int(ini_scan['레지스트 영역2']):
                    data_scan['cal_scan_buffer'] = int(data_scan['scan_buffer']) + (int(ini_scan['레지스트 영역'][-5:]) - int(ini_scan['레지스트 영역2']))
                #'레지스트 영역' 뒤 부터 5자리가 '레지스트 영역2' 보다 작은 경우
                elif int(ini_scan['레지스트 영역'][-5:]) < int(ini_scan['레지스트 영역2']):
                    data_scan['cal_scan_buffer'] = int(data_scan['scan_buffer']) - (int(ini_scan['레지스트 영역2']) - int(ini_scan['레지스트 영역'][-5:]))
                #'레지스트 영역' 뒤 부터 5자리가 '레지스트 영역2' 와 같은 경우
                else:
                    data_scan['cal_scan_buffer'] = data_scan['scan_buffer']

                #'비트' 컬럼 값이 NaN 인 경우
                if pd.isna(data_scan['비트']): 
                    #조건에 따라 계산된 'scan_buffer' 를 이용해서 'FULL_ADDRESS' 값을 생성
                    data_scan['FULL_ADDRESS'] = ini_scan['레지스트 영역'][:3] + str(data_scan['cal_scan_buffer']).rjust(5,'0')

                #'비트' 컬럼 값이 NaN 이 아닌 경우
                else:
                    data_scan['FULL_ADDRESS'] = ini_scan['레지스트 영역'][:3] + str(data_scan['cal_scan_buffer']).rjust(5,'0') +'.' + str(int(data_scan['비트'])).rjust(2, '0') #'비트' 를 int 로 하지 않으면 'DM117000.5.0' 와 같은 형태로 나옴

        #'Tag_group' 의 값이 '태그 그룹' 에 있지만 'scan_buffer' 값이 해당 범위를 벗어나는 경우
        else:
            data_scan['AD_FLAG'] = 'ERROR_SCAN_NO'
    # 'Tag_group' 의 값이 '태그 그룹' 에 없으면 'NO_TAG_GROUP'
    else:
        data_scan['AD_FLAG'] = 'NO_TAG_GROUP'

    return data_scan['cal_scan_buffer'], data_scan['PLC_AREA'], data_scan['AD_FLAG'], data_scan['FULL_ADDRESS']

data_scan_result = data_scan.apply(address, axis=1)

print(data_scan_result)

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

# #컬럼 추가
# data_scan.insert(4, 'cal_scan_buffer', "")
# data_scan.insert(5, 'AD_FLAG', "")
# data_scan.insert(6, 'PLC_AREA', "")
# data_scan.insert(7, 'FULL_ADDRESS', "")

# for i, data_scan in data_scan.iterrows(): #iterrows() 각 행의 인덱스와 데이터 값을 반환한다 --> data_scan 의 행을 반복하면서 각 행의 인덱스와 값을 반환한다
#     #'Tag_group' 의 값이 '태그 그룹' 에 있는지 검사
#     if data_scan['Tag_group'] in ini_scan.loc[:, '태그 그룹'].values: #1개 행마다 값을 비교하기 때문에 row[] 를 사용, loc[인덱스, 컬럼명], : 는 모든 행 선택
#         for j, ini_scan_row in ini_scan.iterrows():
#             #'Tag_group' 의 값이 '태그 그룹' 에 있으면서 'scan_buffer' 값이 'start2', 'end2' 범위에 들어오는 경우
#             if data_scan['Tag_group'] == ini_scan_row['태그 그룹'] and int(data_scan['scan_buffer']) >= int(ini_scan_row['start2']) and int(data_scan['scan_buffer']) <= int(ini_scan_row['end2']): 
#                 #.txt 파일에서 주석처리 부분                                
#                 if ini_scan.at[j, 'off_set'] == 1:
#                     data_scan.at[i, 'AD_FLAG'] = 'ERROR_OFFSET'
#                     break
#                 else:        
#                     data_scan.at[i, 'AD_FLAG'] = 'OK' #'Tag_group' 의 값이 '태그 그룹' 에 있는 data_scan 의 i 번째 행의 'AD_FLAG' 컬럼에 'OK'
#                     data_scan.at[i, 'PLC_AREA'] = ini_scan_row['레지스트 영역'][:3]# 'PLC_AREA' 컬럼에 레지스트 영역의 왼쪽부터 3자리 입력, ini_scan 은 ['레지스트 영역'] 컬럼 전체를 가져오기 때문에 ini_scan_row 를 사용한다, 
#                     #'레지스트 영역' 뒤 부터 5자리가 '레지스트 영역2' 보다 큰 경우
#                     if int(ini_scan.at[j, '레지스트 영역'][-5:]) > int(ini_scan.at[j, '레지스트 영역2']):
#                         data_scan.at[i, 'cal_scan_buffer'] = int(data_scan['scan_buffer']) + (int(ini_scan.at[j, '레지스트 영역'][-5:]) - int(ini_scan.at[j, '레지스트 영역2']))
#                     #'레지스트 영역' 뒤 부터 5자리가 '레지스트 영역2' 보다 작은 경우
#                     elif int(ini_scan.at[j, '레지스트 영역'][-5:]) < int(ini_scan.at[j, '레지스트 영역2']):
#                         data_scan.at[i, 'cal_scan_buffer'] = int(data_scan['scan_buffer']) - (int(ini_scan.at[j, '레지스트 영역2']) - int(ini_scan.at[j, '레지스트 영역'][-5:]))
#                     #'레지스트 영역' 뒤 부터 5자리가 '레지스트 영역2' 와 같은 경우
#                     else:
#                         data_scan.at[i, 'cal_scan_buffer'] = data_scan.at[i, 'scan_buffer']

#                     #조건에 따라 계산된 'scan_buffer' 를 이용해서 'FULL_ADDRESS' 값을 생성
#                     data_scan.at[i, 'FULL_ADDRESS'] = ini_scan_row['레지스트 영역'][:3] + str(data_scan.at[i, 'cal_scan_buffer']).rjust(5,'0')
#                     #'비트' 컬럼 값이 NaN 인 경우
#                     if pd.isna(data_scan['비트']): 
#                         break

#                     #'비트' 컬럼 값이 NaN 이 아닌 경우
#                     else:
#                         data_scan.at[i, 'FULL_ADDRESS'] += '.' + str(int(data_scan['비트'])).rjust(2, '0') #'비트' 를 int 로 하지 않으면 'DM117000.5.0' 와 같은 형태로 나옴
#                         break
#             #'Tag_group' 의 값이 '태그 그룹' 에 있지만 'scan_buffer' 값이 해당 범위를 벗어나는 경우
#             else:
#                 data_scan.at[i, 'AD_FLAG'] = 'ERROR_SCAN_NO'
#     # 'Tag_group' 의 값이 '태그 그룹' 에 없으면 'NO_TAG_GROUP'
#     else:
#         data_scan.at[i, 'AD_FLAG'] = 'NO_TAG_GROUP'

# print(data_scan)

#데이터프레임의 구분자에 따라 접두사와 접미사를 다르게 해서 .csv 파일을 생성하는 중 ing...

# data_scan.to_csv('Nori_tool_address/Outputs/data.csv' #읽어들인 .txt 파일을 .csv 파일로 생성
#            , encoding='utf-8-sig' 
#            , index=False)
