import pandas as pd

path = 'Data_Processing/Pandas/example1/COVID-19-master/csse_covid_19_data/csse_covid_19_daily_reports/'
df = pd.read_csv(path + '04-01-2020.csv', encoding='utf-8-sig')


# print(df.shape) #(2483, 12) 2483행, 12컬럼
# print(df.info()) #not null, type 확인

# #+1에 가까우면, 양의 선형 상관 관계
# #0에 가까우면 상관관계가 없고
# #-1에 가까우면 음의 선형 상관 관계를 가진다
# print(df.corr()) #상관관계 확인

# #결측값 확인
# print(df.isnull().sum()) 
# # df.dropna() #결측값을 포함하는 행을 모두 삭제, subset = ['컬럼명']으로 특정 컬럼값이 없는 행만 삭제할 수 있음

# #결측값을 특정값으로 대체
# nan_data = {'Deaths': 0, 'Recovered':0} #컬럼별로 대체할 값을 다르게 지정할 수 있다
# df.fillna(nan_data)

# #중복값 확인
# print(df[df.duplicated()])#중복된 컬럼만 확인

# #중복행 삭제
# df.drop_ducplicates() #subset='컬렴명', keep='last' 특정 컬럼의 중복값을 제거, 어느 행을 남기고 삭제할지 지정

df1 = pd.DataFrame({
    'id': [1, 2, 3] ,
    'customer_id': [1, 2, 3] ,
    'customer_name': ['Robert', 'Peter', 'Dave']
})
df2 = pd.DataFrame({
    'id': [1, 2, 4] ,
    'order_id': [100, 200, 300] ,
    'order_date': ['2021-01-21', '2021-02-03', '2020-10-01']
})

#데이터프레임 합치기
df_concat = pd.concat([df1, df2]) #axis = 1로 가로로 합칠 수 있다
print(df_concat)

df_merge = pd.merge(df1, df2, on = 'id') #SQL의 INNER JOIN과 같은 기능 how = inner, outer, left, right OUTER JOIN도 가능
print(df_merge)


