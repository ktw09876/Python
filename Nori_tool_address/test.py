import pandas as pd

data_scan = pd.read_csv('Nori_tool_address/data/data1.csv', encoding='cp949')
ini_scan = pd.read_csv('Nori_tool_address/ini_scans/ini1.csv')

# df1 = pd.read_csv("Nori_tool_address/test/example1.csv", header=None) # aaa bbb ccc ddd eee
# df2 = pd.read_csv("Nori_tool_address/test/example2.csv" , header=None) # aaa bbb

result = data_scan[data_scan['Tag_group'].isin(ini_scan['태그 그룹'])]['Tag_group'].tolist() # df2의 첫 번째 열에 존재하는 값만 추출하여 리스트로 반환
df = pd.DataFrame(result)

for i in data_scan.index:
    for j in df.index:
        # if data_scan.iloc[i]['Tag_group'] == df.iloc[j]:
            print(data_scan.iloc[i]['Tag_group'])

# print(result)


