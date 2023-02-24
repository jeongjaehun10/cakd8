import json
from emoji import core

def remove_emoji(item):
    core.replace_emoji(item, replace=' ').replace('\t', '')
with open('./data/data2.json','r') as f:
    data=json.load(f)
count = 0
json_list = []
print(len(data))
for _ in data:
    new_dict = {}
    if core.replace_emoji(_['content'],replace = ' ').replace('\t','') != '':
        new_dict.setdefault("DOCID", 320000+count)
        new_dict.setdefault("title",remove_emoji(_['title']))

        new_dict.setdefault("content",remove_emoji(_['content']))
        new_dict.setdefault('board',_['board'])
        new_dict.setdefault('price',_['price'])
        new_dict.setdefault("url",_['url'])
        json_list.append(new_dict)
    count+=1
print(len(json_list))
with open('./data/data2_new_utf.json','w',encoding='utf-8') as f:
    json.dump(json_list,f)
