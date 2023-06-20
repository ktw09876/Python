import json

# 변수에 문자열로 된 JSON 포멧의 데이터가 있을 경우
data = { "id":"01", "language": "Java", "edition": "third", "author": "Herbert Schildt" }
#'language'컬럼의 데이터의 depth가 2일 때
data['language'] = ['Java', 'C']

with open(r'C:\Users\dhqhf\00_Material(Uploaded)\00_data\test.json', 'w', encoding='utf-8-sig') as json_file:
    json_string = json.dump(data, json_file, indent=2)