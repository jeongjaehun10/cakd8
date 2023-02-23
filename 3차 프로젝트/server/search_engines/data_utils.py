import re
from .similarity import *
from .index import *
# file_path = 'text.txt'
def read_json(file_path):
    json_objs_list = []
    li=os.listdir(file_path)
    for i in li:
        if i.split('.')[1] == 'json':
            with open(file_path+i) as f:
                contexts = f.read()
                contexts = re.sub(r'[“”]', '"', contexts)
                json_objs = json.loads(contexts)
                json_objs_list += json_objs
    return json_objs_list
# input_text = input("문장 : ")
# input_nbest = int(input("개수 : "))

def merge_file(file_list):
    json_objs_list = []
    for i in file_list:
        if i.file_name.split('.')[1] == 'json':
            fpath = i.file_dir + i.file_name
            with open(fpath) as f:
                contexts = f.read()
                contexts = re.sub(r'[“”]', '"', contexts)
                json_objs = json.loads(contexts)
                json_objs_list += json_objs

    return json_objs_list


def get_similarity_in_document(input_text,input_nbest,json_objs):
    for json_obj in json_objs:
        indicies = get_idx(input_text, json_obj['text'])
        embeddings = get_pooleroutput(indicies)
        json_obj['similarity'] = get_total_scores(embeddings[0], embeddings[1])
    json_objs.sort(key=lambda x : -x['similarity'])
    for i,json_obj in enumerate(json_objs):
        json_obj['nbest'] = i+1
        if (i+1) == input_nbest: break;
    return json_objs
def search_in_es(q,n):
    que=q.replace('[^A-Za-z0-9가-힣]', '')
    query_with_tag=mecab.pos(que)
    print(query_with_tag)
    print(mecab.tagset)
    query = []
    for item in query_with_tag:
        if (item[1] == 'XR') | (item[1] == 'NNG') | (item[1] == 'VV') | (item[1] == 'NNB') | (item[1] == 'NNP') | (item[1] == 'VA') | (item[1] == 'NP')  | (item[1] == 'SN')| (item[1] == 'NA')| (item[1] == 'NR')| (item[1] == 'SL'):
            query.append(item[0])
    print(mecab.pos(que)[0][0])
    print(query)
    data = []  # 반환할 데이터를 담을 리스트를 초기화합니다
    for item in query:
        query = {
            "query": {
                "multi_match": {
                    "query": item,
                    "fields": ["title", "content","title_morphs","content_morphs"]
            }
        }
        }
        res =es.search(index = 'my_index',body = query)
        hits = res.get('hits', {}).get('hits', [])  # 실제 데이터가 있는 hits 리스트를 추출합니다
        # 각각의 문서에 대해서 필요한 정보만 추출하여 data 리스트에 추가합니다
        for hit in hits:
            source = hit.get('_source', {})
            item = {
                'title': source.get('title', ''),
                'content': source.get('content', ''),
                'title_dpr': source.get('title_dpr', []),
                'content_dpr': source.get('content_dpr', []),
            }
            if item not in data:
                data.append(item)
    for item in data:
        question=model(tokenizer(q, return_tensors="pt",truncation=True,max_length=512)["input_ids"]).pooler_output
        ctx=torch.tensor(item['content_dpr'])
        title=torch.tensor(item['title_dpr'])
        score1=get_total_scores(question,ctx)
        score2=get_total_scores(question,title)
        item.setdefault('score',score1+score2)
    sorted_list = sorted(data, key=lambda x: x['score'], reverse=True)
    print(len(sorted_list))
    return sorted_list[:n]
