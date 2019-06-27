import json

def config_load():
    with open('data/config.json', 'r', encoding='utf-8') as doc:
        return json.load(doc)
    
