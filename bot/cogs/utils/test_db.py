from db import *
import asyncio




async def test_db():
    #test 1 - reset settings for guild 1 and then retrieve them
    test_config = {"test_field":"test_value"}
    await updateCogSettings(1,"test_cog",test_config)
    s = await getSettings(1,cog="test_cog")
    
    if s != test_config:
        print("TEST 1 FAILED")
        print(f"EXPECTED {test_config}  GOT {s}")
        return False

    #test 2 - change it to something different
    test_config2 = {"test_field":"test_value2"}
     
    await updateCogSettings(1,"test_cog",test_config2)
    s = await getSettings(1,cog="test_cog")
    
    if s != test_config2:
        print("TEST 2 FAILED")
        print(f"EXPECTED {test_config2}  GOT {s}")
        return False    


    #test3 - update settings with cog = None

    test_config3 = {"test_field":"test_value3"}
    await updateSettings(1,{"test_cog":test_config3})

    s = await getSettings(1,cog="test_cog")
    
    if s != test_config3:
        print("TEST 3 FAILED")
        print(f"EXPECTED {test_config3}  GOT {s}")
        return False    




    print("DB TESTS PASSED")


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.ensure_future(test_db()))