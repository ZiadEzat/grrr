import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client.ram


def getSettings(server_id, cog=None):
    s = db['settings'].find_one({'server_id': server_id})
    if cog == None:
        return s
    if s == None:
        return {'enabled': False}
    else:
        return s.get(cog, {'enabled': False})


def updateCogSettings(server_id, cog_name, new_settings):
    db['settings'].update_one({'server_id': server_id}, {'$set': {cog_name: new_settings}}, upsert=True)


def updateSettings(server_id, new_settings):
    db['settings'].update_one({'server_id': server_id}, {'$set': new_settings}, upsert=True)
