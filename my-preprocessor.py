import json
data = open('data.json', encoding="utf-8-sig")
my_json = json.load(data)

for i in my_json['content']:
    i['text'] = i['Sentence']
    i["id_str"] = i['Season'] + "_" +i['Episode'] + "_"+ i['Name']

texts = []
for i in my_json['content']:
    texts.append(json.dumps(i))

text = '\n\n\n'.join(texts)

f = open("./data/tweetdata.txt", "w")
f.write(text)
f.close()

