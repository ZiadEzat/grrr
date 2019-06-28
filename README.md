# grrr
Discord Hack week bot by Grrrrrrrr team 

## Features

- Join Log: when a new user joins it will tell the mods that they are 


## Project Description
A discord bot that will keep communities a safe environment by censoring insults and spam through the use of neural networks. This bot will scan all messages sent within a server (minus the excluded channels ie: mod talk) and run their contents through a few neural networks that are trained on spam copy pastas and troll messages.   


### Setup
This bot is very simple to setup for yourself!

1. Firstly we need to install MongoDB to your machine where you will be hosting this bot!

    - [Windows Install Instructions](https://medium.com/@LondonAppBrewery/how-to-download-install-mongodb-on-windows-4ee4b3493514)
    - For Mac just run `brew install mongo` and make sure its running with `brew services start mongodb`
    - Ubuntu: `sudo apt-get install mongodb`

2. Next to install the dependencies please run these commands```pip install -r requirements.txt```

3. Then if you want to test your mongo setup there is a file named `/bot/cogs/utils/test_db.py` that you can run. You should see **DB TESTS PASSED** if everything worked fine

4. Finally to start the bot portion of the application run the `run_bot.sh` file!
