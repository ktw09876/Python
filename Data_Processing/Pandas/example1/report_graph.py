import pandas as pd

df = pd.read_csv("result_df.csv")
# print(df.shape) #(187, 149)

#국가 정보 가져오기
country_path = 'Data_Processing/Pandas/example1/COVID-19-master/csse_covid_19_data/'
country_info = pd.read_csv(
        country_path #경로
        + 'UID_ISO_FIPS_LookUp_Table.csv' #파일명
        , encoding='utf-8-sig' #인코딩 지정
        , keep_default_na=False #‘’, ‘#N/A’, ‘#N/A N/A’, ‘#NA’, ‘-1.#IND’, ‘-1.#QNAN’, ‘-NaN’, ‘-nan’, ‘1.#IND’, ‘1.#QNAN’, ‘’, ‘N/A’, ‘NA’, ‘NULL’, ‘NaN’, ‘n/a’, ‘nan’, ‘null’ 와 같은 값이 있으면 그대로 읽어라
        , na_values='' #결측치가 있다면 ''(빈 값)으로 읽어라
    )
# print(country_info.head())
# print(country_info.shape) #3560행, 13컬럼

# Namibia의 iso2값은 'NA'
# print(country_info[country_info['Country_Region'] == 'Namibia'])

#국가 정보 파일에서 필요한 컬럼만 가져온다
country_info = country_info[['iso2', 'Country_Region']]
country_info = country_info.drop_duplicates(subset='Country_Region', keep='first')
# print(country_info.shape) #(180, 2)

#daily_report정보와 국가 정보를 합친다
df_final_country = pd.merge(df, country_info, how='left', on='Country_Region')

#혹시 iso2값이 없는 경우가 있나?
# print(df_final_country.isnull().sum()) #9개
# print(df_final_country[df_final_country['iso2'].isnull()])

#iso2값이 없는 경우 삭제
df_final_country = df_final_country.dropna(subset=['iso2'])

# #국기 이미지 가져오기
# def create_flag_link(iso2):
#     flag_link = 'https://flagcdn.com/48x36/' + iso2 + '.png'
#     return flag_link

# df_final_country['iso2'] = df_final_country['iso2'].apply(create_flag_link)
# # print(df_final_country)


#이미지 생성
def create_flag_link(iso2):
    if iso2 == 'AS':
        iso2 = 'US'
    iso2 = iso2.lower()
    flag_link = "https://public.flourish.studio/country-flags/svg/" + iso2 + ".svg"
    return flag_link

df_final_country['iso2'] = df_final_country['iso2'].apply(create_flag_link)







#'iso2'컬럼명 위치 조정
#컬럼명을 리스트로 가져오기
cols = df_final_country.columns.tolist()

#삭제 후 원하는 위치에 삽입
cols.remove('iso2')
cols.insert(1, 'iso2')
df_final_country = df_final_country[cols]

#컬럼명 변경
cols[1] = 'Country_Flag'
df_final_country.columns = cols
# print(df_final_country)

df_final_country.to_csv('final_df.csv', encoding='utf-8-sig')