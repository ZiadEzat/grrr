import json
"""
    config_load() - callable function for parsing configuration files
"""
def config_load():
    with open('data/config.json', 'r', encoding='utf-8') as doc:
        return json.load(doc)
    
