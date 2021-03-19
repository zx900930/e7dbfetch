# Autor: Xavier Xiong
# Only support python 3+
# To update data just run: py -3 fetch.py
import urllib.request, json, os

path = os.path.dirname(os.path.abspath(__file__))
print('Working directory: '+path)
os.chdir(path)
os.makedirs('../json/', exist_ok=True)

langs=[{"url": "en","code": "en", "name": "English"}, {"url": "ja","code": "ja", "name": "Japanese"}, {"url": "ko","code": "ko", "name": "Korean"}, {"url": "fr","code": "fr", "name": "French"}, {"url": "cn","code": "cn", "name": "Chinese Simplified"}, {"url": "zht","code": "tw", "name": "Chinese Traditional"}]
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')]
urllib.request.install_opener(opener)
print('Start generating js files...')

for lang in langs:
    url = 'https://api.epicsevendb.com/hero?lang='+lang.get("url")
    urllib.request.urlretrieve(url, './json/'+lang.get("code")+'.characters.json')
    with open('./json/'+lang.get("code")+'.characters.json', encoding='utf-8') as f:
        data = json.load(f)

    results=data["results"]

    characters = {}
    for item in results:      
        if item.get('rarity') > 1:
            characters[item.get('_id')]=item.get('name')

    if lang.get("code") == 'en':
        characters_en=characters
        characters_merged=characters
    else:
        characters_merged ={}
        for key, name in iter(characters_en.items()):
            characters_merged[name] = characters[key]
      
    back_json=json.dumps(characters_merged, indent = 4, ensure_ascii=False)
    back_json = back_json
    
    with open("./json/"+lang.get("code")+".characters.json", "w", encoding='utf-8') as outfile: 
        outfile.write(back_json)

    url = 'https://api.epicsevendb.com/artifact?lang='+lang.get("url")
    urllib.request.urlretrieve(url, './json/'+lang.get("code")+'.artifacts.json')
    
    with open('./json/'+lang.get("code")+'.artifacts.json', encoding='utf-8') as f:
        data = json.load(f)
    
    results=data["results"]
    
    artifacts = {}
    for item in results:
        if item.get('rarity') > 2:
            artifacts[item.get('_id')]=item.get('name')
    
    if lang.get("code") == 'en':
        artifacts_en=artifacts
        artifacts_merged=artifacts
    else:
       artifacts_merged ={}
       for key, name in iter(artifacts_en.items()):
            artifacts_merged[name] = artifacts[key]


    back_json=json.dumps(artifacts_merged, indent = 4, ensure_ascii=False)
    back_json = back_json

    with open("./json/"+lang.get("code")+".artifacts.json", "w", encoding='utf-8') as outfile: 
        outfile.write(back_json) 
    print('File saved to:'+os.path.abspath("./json/"+lang.get("code")+".artifacts.json"))
    
    full={}
    full.update(characters_merged)
    full.update(artifacts_merged)

    back_json=json.dumps(full, indent = 4, ensure_ascii=False)
    with open("./json/"+lang.get("code")+".full.json", "w", encoding='utf-8') as outfile: 
        outfile.write(back_json) 
    print('File saved to:'+os.path.abspath("./json/"+lang.get("code")+".full.json"))
    print(lang.get("name")+' Finish')
