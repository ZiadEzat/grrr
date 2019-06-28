from motor import motor_asyncio as mongod
client = mongod.AsyncIOMotorClient('localhost', 27017)
db = client.ram





async def getSettings(server_id,cog=None):

    s = await db['settings'].find_one({'server_id':server_id})
    # print(f"s {s} cog {cog}")
    if cog == None:
        return s

    if s == None:
        return {'enabled':False}

    else:   

        return s.get(cog,{'enabled':False})


async def updateCogSettings(server_id,cog_name,new_settings):

    await db['settings'].update_one({'server_id':server_id}, {'$set': { cog_name : new_settings}},upsert=True)
    

async def updateSettings(server_id,new_settings):

    await db['settings'].update_one({'server_id':server_id}, {'$set': new_settings},upsert=True)



    

