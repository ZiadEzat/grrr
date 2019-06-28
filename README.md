![RAM](https://imgur.com/KB18eCZ.png)
# Rage Against the Machine (RAM)
Discord Hack Week  Moderation Bot by Grrrrrrrr team
#### Contributers:

- J_C___#8947
- Marto#0874
- Nolewit#9352
- Ziad (RvPso)#3363
- Potato#6037

## Features

- Join Log: When a new user joins the server it will tell the mods about that user
![Join Logs](https://i.imgur.com/D7fKe8o.png "Join Logs")
- Reaction Roles: Users can add custom roles to themselves with this highly customizable, easily configurable module.
- AutoModerator: This is the largest and most exciting feature of RAM. This module acts as a much more robust version of Discord's Explicit Content Feature. Passing all your messages through [Google's Perspective API](https://www.perspectiveapi.com/#/home) RAM can determine if what users are saying is insulting or demeaning to others! We designed this feature to take the pressure off of a lot of moderators shoulders so they can stop worrying so much about message sensoring.
![Dicrors bot](https://cdn.discordapp.com/attachments/591700394820763682/594232336132866050/Screen_Shot_2019-06-28_at_2.26.00_PM.png)
- Server Level Settings: This bot was built to be hosted by one individual and spread across the discord mulit-verse using invite links. Each server can enable and disable commands and features using **!enable [command]** or **!disable [command]** as we will show more of later.





## Project Description
A discord bot that will keep communities a safe environment by censoring insults and spam through the use of neural networks. This bot will scan all messages sent within a server (minus the excluded channels ie: mod talk) and run their contents through a few neural networks that are trained on spam copy pastas and troll messages.

## How to use:
!enable autoMod: Allows bot to delete messages flagged by perspective api


### Hosting your own instance of RAM
This bot is very simple to setup for yourself!
1. Obligatory clone the Repo.
1. Duplicate the config.json.example file to be config.json and fill out the fields present
1. Next we need to install MongoDB to your machine where you will be hosting this bot!

    - [Windows Install Instructions](https://medium.com/@LondonAppBrewery/how-to-download-install-mongodb-on-windows-4ee4b3493514)
    - For Mac just run `brew install mongo` and make sure its running with `brew services start mongodb`
    - Ubuntu: `sudo apt-get install mongodb`

2. Next to install the dependencies please run these commands```pip install -r requirements.txt```

3. Then if you want to test your mongo setup there is a file named `/bot/cogs/utils/test_db.py` that you can run. You should see **DB TESTS PASSED** if everything worked fine

4. Finally to start the bot portion of the application run the `run_bot.sh` file!
