import pandas as pd
import cx_Oracle
import numpy as np

#.csv 파일이 한 개 경우
# data_scan = pd.read_csv('Nori_tool_address/data/data1.csv', encoding='cp949')

# #.txt 파일이 두 개 이상 경우
data_path = 'Nori_tool_address/data/'
data_list = [
        'data1.csv',
        'data2.csv'
    ]

#데이터프레임 생성, '라인 구분' 컬럼 추가
data_dfs = []
for data_name in data_list:
    df = pd.read_csv(data_path + data_name, encoding='cp949') #dtype={'비트': 'Int64'} '비트' 컬럼의 값을 insert 할 수 있도록 형변환 dtype={'비트': 'Int64'}, 
    df['라인 구분'] = df['Tag_group'].str.slice(0,3)
    data_dfs.append(df)

data_scan = pd.concat(data_dfs, ignore_index=True) #data .csv 읽어들인 데이터프레임을 하나로 합친다
ini_scan = pd.read_csv('Nori_tool_address/ini_scans/ini1.csv') #기준정보 .csv

#컬럼 추가
data_scan.insert(4, 'cal_scan_buffer', "")
data_scan.insert(5, 'AD_FLAG', '')
data_scan.insert(6, 'PLC_AREA', "")
data_scan.insert(7, 'FULL_ADDRESS', "")

#처리 로직
for i, data_scan_row in data_scan.iterrows(): #iterrows() 각 행의 인덱스와 데이터 값을 반환한다 --> data_scan 의 행을 반복하면서 각 행의 인덱스와 값을 반환한다
    for j, ini_scan_row in ini_scan.iterrows():
        #'Tag_group' 의 값이 '태그 그룹' 에 있는지 검사
        if data_scan_row['Tag_group'] in ini_scan.loc[:, '태그 그룹'].values: #1개 행마다 값을 비교하기 때문에 row[] 를 사용, loc[인덱스, 컬럼명], : 는 모든 행 선택
            #'Tag_group' 의 값이 '태그 그룹' 에 있으면서 'scan_buffer' 값이 'start2', 'end2' 범위에 들어오는 경우
            if data_scan_row['Tag_group'] == ini_scan_row['태그 그룹'] and int(data_scan_row['scan_buffer']) >= int(ini_scan_row['start2']) and int(data_scan_row['scan_buffer']) <= int(ini_scan_row['end2']): 
                #.txt 파일에서 주석처리 부분
                if ini_scan.at[j, 'off_set'] == 1:
                    data_scan.at[i, 'AD_FLAG'] = 'ERROR_OFFSET'
                    break
                else:
                    #
                    data_scan.at[i, 'AD_FLAG'] = 'OK' #'Tag_group' 의 값이 '태그 그룹' 에 있는 data_scan 의 i 번째 행의 'AD_FLAG' 컬럼에 'OK'
                    data_scan.at[i, 'PLC_AREA'] = ini_scan_row['레지스트 영역'][:3]# 'PLC_AREA' 컬럼에 레지스트 영역의 왼쪽부터 3자리 입력, ini_scan 은 ['레지스트 영역'] 컬럼 전체를 가져오기 때문에 ini_scan_row 를 사용한다, 
                    #'레지스트 영역' 뒤 부터 5자리가 '레지스트 영역2' 보다 큰 경우
                    if int(ini_scan.at[j, '레지스트 영역'][-5:]) > int(ini_scan.at[j, '레지스트 영역2']):
                        data_scan.at[i, 'cal_scan_buffer'] = int(data_scan_row['scan_buffer']) + (int(ini_scan.at[j, '레지스트 영역'][-5:]) - int(ini_scan.at[j, '레지스트 영역2']))
                    #'레지스트 영역' 뒤 부터 5자리가 '레지스트 영역2' 보다 작은 경우
                    elif int(ini_scan.at[j, '레지스트 영역'][-5:]) < int(ini_scan.at[j, '레지스트 영역2']):
                        data_scan.at[i, 'cal_scan_buffer'] = int(data_scan_row['scan_buffer']) - (int(ini_scan.at[j, '레지스트 영역2']) - int(ini_scan.at[j, '레지스트 영역'][-5:]))
                    #'레지스트 영역' 뒤 부터 5자리가 '레지스트 영역2' 와 같은 경우
                    else:
                        data_scan.at[i, 'cal_scan_buffer'] = data_scan.at[i, 'scan_buffer']

                    #조건에 따라 계산된 'scan_buffer' 를 이용해서 'FULL_ADDRESS' 값을 생성
                    data_scan.at[i, 'FULL_ADDRESS'] = ini_scan_row['레지스트 영역'][:3] + str(data_scan.at[i, 'cal_scan_buffer']).rjust(5,'0')
                    #'비트' 컬럼 값이 NaN 인 경우
                    if pd.isna(data_scan_row['비트']): 
                        break

                    #'비트' 컬럼 값이 NaN 이 아닌 경우
                    else:
                        data_scan.at[i, 'FULL_ADDRESS'] += '.' + str(int(data_scan_row['비트'])).rjust(2, '0') #'비트' 를 int 로 하지 않으면 'DM117000.5.0' 와 같은 형태로 나옴
                        break
            #'Tag_group' 의 값이 '태그 그룹' 에 있지만 'scan_buffer' 값이 해당 범위를 벗어나는 경우
            else:
                data_scan.at[i, 'AD_FLAG'] = 'ERROR_SCAN_NO'
        #'Tag_group' 의 값이 '태그 그룹' 에 없으면 'NO_TAG_GROUP'
        else:
            data_scan.at[i, 'AD_FLAG'] = 'NO_TAG_GROUP'



#오라클 연동
user = 'TEST_USER'
password = '1234'
dns = 'localhost:1521/xepdb1'

connection = cx_Oracle.connect(user, password, dns) #연결
cursor = connection.cursor() #커서 -->쿼리문에 의해 반환되는 결과값을 저장하는 메모리 공간



#데이터프레임 가공
data_scan_ok = data_scan[data_scan['AD_FLAG'] == 'OK'] #데이터프레임의 'AD_FLAG' 값이 'OK' 인 대상만 insert 하겠다
data_scan_ok['비트'] = data_scan_ok['비트'].apply(lambda x: None if pd.isna(x) else x)


#'비트' 컬럼의 None 값을 인서트 ing....
# # None 값을 Null 값으로 변환하는 함수 정의
# def none_to_null(data_scan_ok):
#     return data_scan_ok if data_scan_ok is not None else cx_Oracle.NULL

# # 데이터프레임에서 None 값을 Null 값으로 변환
# data_scan = data_scan_ok.applymap(none_to_null)

# data_scan_ok = data_scan_ok.where(pd.notnull(data_scan_ok), None) #형변환
# data_scan_ok = data_scan_ok.fillna(None, method='ffill') #형변환
# data_scan_ok = data_scan_ok.fillna('') #형변환
print(data_scan_ok)

#insert 쿼리
insert_sql = """ 
        INSERT INTO address VALUES(:TAG_GROUP, :TAG_NAME, :SCAN_BUFFER, :BIT, :CAL_SCAN_BUFFER, :AD_FLAG, :PLC_AREA, :FULL_ADDRESS, :GUBUN)
    """ 
cursor.executemany(insert_sql, data_scan_ok.values.tolist()) #insert, #데이터프레임을 2차원 리스트로
connection.commit() #전체 연결에 대한 트랜잭션 커밋
# cursor.execute("commit") #특정 커서에 대한 커밋

#들어간 갯수 확인
cursor.execute('select count(*) from address')
row = cursor.fetchone()
print('삽입된 data는 총 ' + str(row[0]) + '개 입니다')



cursor.close()
connection.close()

#데이터프레임의 구분자에 따라 접두사와 접미사를 다르게 해서 .csv 파일을 생성하는 중 ing...

# data_scan.to_csv('Nori_tool_address/Outputs/data.csv' #읽어들인 .txt 파일을 .csv 파일로 생성
#            , encoding='utf-8-sig' 
#            , index=False)