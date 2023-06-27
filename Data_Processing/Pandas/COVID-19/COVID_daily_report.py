import pandas as pd
import json
import os

# #daily_report.csv 읽기
daily_report_path = 'Data_Processing/Pandas/COVID-19/COVID-19-master/csse_covid_19_data/csse_covid_19_daily_reports/'
# daily_report_df = pd.read_csv(daily_report_path + '01-22-2020.csv', encoding='utf-8-sig')
# # print(daily_report_df.head())

# #daily_reports에 날짜별로 컬럼명이 다른 경우가 있음
# try:
#     daily_report_df = daily_report_df[['Province_State', 'Country_Region', 'Confirmed']]  #내가 원하는 특정 컬럼만 가지고 데이터프레임을 만든다
# except:
#     daily_report_df = daily_report_df[['Province/State', 'Country/Region', 'Confirmed']]  #만약 ['Province/State', 'Country/Region', 'Confirmed']라는 컬럼명이 있다면 
#     daily_report_df.columns = ['Province_State', 'Country_Region', 'Confirmed'] #내가 원하는 컬럼명으로 바꿔서 가져오겠다
    
# # print(daily_report_df.info())
# daily_report_df = daily_report_df.dropna(subset=['Confirmed']) #'Confirmed'컬럼이 없는 행은 삭제
# daily_report_df = daily_report_df.astype({'Confirmed': 'int64'}) #'Confirmed'의 타입 변경
# # print(daily_report_df.head())
# # print(daily_report_df.shape) #29행, 13컬럼

# #국가 정보 가져오기
# country_path = 'Data_Processing/Pandas/COVID-19/COVID-19-master/csse_covid_19_data/'
# country_info = pd.read_csv(country_path + 'UID_ISO_FIPS_LookUp_Table.csv', encoding='utf-8-sig')
# # print(country_info.head()) #iso2가 국가기호 2자리
# # print(country_info.shape) #3560행, 13컬럼

# #daily_report_df와 country_info 합치기
# test_df = pd.merge(daily_report_df, country_info, how='left', on='Country_Region')

# #non-null 데이터 개수가 서로 다른걸 보니 조인이 제대로 안되는 거 같음
# # print(test_df.info())
# # print(test_df.isnull().sum())

# #'Country_Region'이 일반적인 국가명이 아닌 다른 여러 데이터가 있는 경우가 있음 그래서 조인이 안됐구나
# non_df = test_df[test_df['iso2'].isnull()]
# # print(non_df.head())

#국가별로 다양한 'Country_Region'값을 한가지로 만들어놓은 json파일
json_path = 'Data_Processing/Pandas/COVID-19/COVID-19-master/csse_covid_19_data/'
with open(json_path + 'country_convert.json', 'r', encoding='utf-8-sig') as json_file:
    json_data = json.load(json_file)
    # print(json_data.keys())

# #'Country_Region'컬럼의 특정 값을 변경하는 함수 정의
# def Country_Region_replace(row): 
#     if row['Country_Region'] in json_data: 
#         row['Country_Region'] = json_data[row['Country_Region']]
    
#     return row

# #apply()를 활용해서 'Country_Region'컬럼의 데이터를 변경
# daily_report_df = daily_report_df.apply(Country_Region_replace, axis=1)

# #'Country_Region'값을 변경한 daily_report_df와 country_info 합치기
# join_df = pd.merge(daily_report_df, country_info, how='left', on='Country_Region')
# # print(join_df.shape)

# #'Country_Region'에 결측값이 없음 --> 모두 join 됐음
# # print(join_df.info())
# # print(join_df.isnull().sum())

# #daily_report의 'Country_Region'컬럼의 국가명을 바꾼 데이터로 국가별 확진자수를 구한다
# sum_df = daily_report_df.groupby('Country_Region').sum()
# print(sum_df.head())

#'Country_Region'컬럼의 특정 값을 변경하는 함수 정의
def Country_Region_replace(row): 
    if row['Country_Region'] in json_data: 
        return json_data[row['Country_Region']]
    
    return row['Country_Region']

#위의 과정을 활용해서 daily_report 전처리하는 함수
def create_daily_report_df(filename):
    #1.daily_report.csv 읽기
    df = pd.read_csv(daily_report_path + filename, encoding='utf-8-sig')
    try:
        df = df[['Country_Region', 'Confirmed']]  #내가 원하는 특정 컬럼만 가지고 데이터프레임을 만든다
    except:
        df = df[['Country/Region', 'Confirmed']]  #만약 ['Country/Region', 'Confirmed']라는 컬럼명이 있다면 
        df.columns = ['Country_Region', 'Confirmed'] #내가 원하는 컬럼명으로 바꿔서 가져오겠다
    
    df = df.dropna(subset=['Confirmed']) #'Confirmed'컬럼이 없는 행은 삭제
    df['Country_Region'] = df.apply(Country_Region_replace, axis=1) # #apply()를 활용해서 'Country_Region'컬럼의 데이터를 변경
    df = df.astype({'Confirmed': 'int64'}) #'Confirmed'의 타입 변경
    df = df.groupby('Country_Region').sum() #'Country_Region'별로 확진자를 합친다

    #파일명을 날짜로 바꾸고 'Confirmed'컬럼명 변경
    date_column = filename.split('.')[0].lstrip('0').replace('-', '/')
    df.columns = [date_column]
    return df

#test
# print(create_daily_report_df('01-22-2020.csv'))

#파일명을 가져와서 컬럼명을 파일명의 날짜로 바꾸고 전체 날짜의 국가별 확진자수를 구하는 함수
def create_final_df(path):
    file_list = os.listdir(path) #해당 경로의 파일명을 리스트형태로 가져온다
    csv_list = list()
    first_df = True

    for file in file_list:
        if file.split('.')[-1] == 'csv': #확장자가 '.csv'가 아닌 경우도 있을 수 있으니 만약 파일명의 가장 마지막'.'부터 끝까지가 'csv'라면
            csv_list.append(file) #리스트에 추가
        csv_list.sort()

    for file in csv_list:
        df = create_daily_report_df(file)
        #처음 생성된 df
        if first_df:
            final_df = df
            first_df = False
        #두번째 생성되는 df부터는 full outer join으로 데이터를 합쳐 나간다
        else:
            final_df = pd.merge(final_df, df, how='outer', left_index=True, right_index=True)

    #결측치를 모두 0으로 바꾸고 타입을 정수형으로
    final_df = final_df.fillna(0).astype('int64')
    return final_df

#원본 데이터 가공
df = create_final_df(daily_report_path)
# print(df.head())
# print(df.shape)



#가공된 데이터 저장
df.to_csv('result_df.csv', encoding='utf-8-sig')



