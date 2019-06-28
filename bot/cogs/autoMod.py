
from discord.ext import commands
from discord.ext.commands import bot
import discord
from .utils.db import *

import requests
import json
import re


class autoMod(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot
        self.payload = {'key': bot.config['perspective_key']}
        
        self.headers = {'Content-Type': 'application/json'}
        self.treshold = 0.9
        self.numberOfFiltersAboveTresholdToFilter = 2
        self.debug = True
    
    async def countEmojis(self, message: discord.Message):
        count = len(re.findall("(\:[a-z_1-9A-Z]+\:)", message.content))  # custom emojis
        if count == 0:  # Test for Unicode Emojis
            count = len(re.findall('(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|'
                                   '\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])', message.content))
        return count
    
    async def getSettings(self,server_id):
        return await getSettings(server_id,cog="autoMod")
    
    @commands.Cog.listener()
    async def on_message(self,message):
        s = await self.getSettings(message.guild.id)
        if not s['enabled'] or message.author.bot:
            return
        
        response = self.get_toxicity(message.content)
        response = response['attributeScores'.title()]
        msg = "String: " + message.content + "\n"
        scores = [ k for k,v in response.items()  if v['summaryScore']['value'] >= self.treshold ]
        if self.debug:
            for k,v in response.items():
                msg += f"{k} = {v['summaryScore']['value']} \n"
            await message.channel.send(msg)
        if len(scores) >= self.numberOfFiltersAboveTresholdToFilter:
            # print(scores)
            await message.delete()
            embed = await self.create_log(message, scores)
            # TODO: Send log messages to log channel specified on emable if none specified send no logs
            await message.channel.send(embed=embed)
            return
    

    async def create_log(self, message, reasons):
        embed = discord.Embed(title=f"Message removed in {message.channel.name}")
        embed.add_field(name=f"Message:", value=f"{message.content}")
        embed.add_field(name=f"Author:", value=f"{message.author.name}")
        for reason in reasons:
            embed.add_field(name=f"Reason:", value=f"{reason}")
        return embed
    
    
    
    def get_toxicity(self, comment, language='en'):
        languages = ['en', 'fr', 'es']
        if language not in languages:
            raise Exception("Invalid Language for toxicity report")
        data = {'comment': {'text': comment},
            'languages': [language],
            'requestedAttributes': {
                'TOXICITY':{},
                    "THREAT":{},
                        "INSULT":{},
                            "PROFANITY":{},
                                "SEXUALLY_EXPLICIT":{}
                                }
        }
        response = self._send_request(data)
        return response


def _send_request(self, data):
    r = requests.post("https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
                      params=self.payload,
                      headers=self.headers,
                      json=data)
    if r.status_code != 200:
        raise Exception("Error Making Your Request")
    return json.loads(r.text)



def setup(bot):
    bot.add_cog(autoMod(bot))
