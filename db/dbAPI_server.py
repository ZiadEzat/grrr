import config_load as cl
from flask import Flask
from flask import request
from motor import motor_asyncio as mongod

client = mongod.AsyncIOMotorClient('localhost', 27017)
db = client.ram


async def getSettings(server_id, cog=None):
    s = await db['settings'].find_one({'server_id': server_id})
    if cog == None:
        return s
    if s == None:
        return {'enabled': False}
    else:
        return s.get(cog, {'enabled': False})


async def updateCogSettings(server_id, cog_name, new_settings):
    await db['settings'].update_one({'server_id': server_id}, {'$set': {cog_name: new_settings}}, upsert=True)


async def updateSettings(server_id, new_settings):
    await db['settings'].update_one({'server_id': server_id}, {'$set': new_settings}, upsert=True)


app = Flask(__name__)

Akey = cl.config_load()['key']


@app.route('/api/<int:server_id>', methods=['POST', 'GET'])
def accept(server_id):
    if request.args.get("key") == Akey:
        if request.method == 'GET':
            try:
                settings = dict(getSettings(server_id))
                print()
                return '200'
            except Exception as e:
                return '500'
        else:
            return '500'
    #     elif request_type == 'POST':
    #         try:
    #             if db.get_settings(str(channel)):
    #                 if request.args.get("sc") == 's':
    #                     db.set_settings(channel,{'emoji':request.args.get("emoji"), 'copypasta':request.args.get("copypasta"), 'troll':request.args.get("troll"), 'insult':request.args.get("insult"),'alt':request.args.get("alt")})
    #                     return '200'
    #                 elif request.args.get("sc") == 'c':
    #                     db.set_coefs(channel,{'troll':request.args.get('troll'), 'insult':request.args.get("insult")})
    #                     return '200'
    #                 else:
    #                     return '500'
    #             else:
    #                 if request.args.get("sc") == 's':
    #                     db.create_settings(channel,{'emoji':request.args.get("emoji"), 'copypasta':request.args.get("copypasta"), 'troll':request.args.get("troll"), 'insult':request.args.get("insult"),'alt':request.args.get("alt")})
    #                     return '200'
    #                 elif request.args.get("sc") == 'c':
    #                     db.create_coefs(channel,{'troll':request.args.get('troll'), 'insult':request.args.get("insult")})
    #                     return '200'
    #                 else:
    #                     return '500'
    #         except Exception:
    #             return '500'
    # else:
    #     return '500'
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2048)
