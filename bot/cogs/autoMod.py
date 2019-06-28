import datetime
import json
import re

import discord
import requests
from discord.ext import commands

from .utils.db import *


class AutoMod(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot
        self.payload = {'key': bot.config['perspective_key']}
        
        self.headers = {'Content-Type': 'application/json'}
        self.treshold = 0.9
        self.numberOfFiltersAboveTresholdToFilter = 2
        self.emojiThreshhold = 3
        self.debug = False
    
    async def countEmojis(self, message: discord.Message):
        count = len(re.findall("(\:[a-z_1-9A-Z]+\:)", message.content))  # custom emojis
        if count == 0:  # Test for Unicode Emojis
            count = len(re.findall('(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|'
                                   '\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])', message.content))
        return count
    
    async def getSettings(self,server_id):
        return await getSettings(server_id, cog="AutoMod")
    
    @commands.Cog.listener()
    async def on_message(self,message):
        s = await self.getSettings(message.guild.id)
        if not s['enabled'] or message.author.bot:
            return
        if await self.countEmojis(message) > self.emojiThreshhold:
            await message.delete()
            if s['channel']:
                embed = await self.create_log(message, ['Emoji Spam'])
                return await self.bot.get_channel(s['channel']).send(embed=embed)

        
        response = self.get_toxicity(message.content)
        response = response['attributeScores']
        msg = "String: " + message.content + "\n"
        scores = [ k for k,v in response.items()  if v['summaryScore']['value'] >= self.treshold ]
        if self.debug:
            for k,v in response.items():
                msg += f"{k} = {v['summaryScore']['value']} \n"
            await message.channel.send(msg.title())
        if len(scores) >= self.numberOfFiltersAboveTresholdToFilter:
            await message.delete()

            # TODO: Send log messages to log channel specified on emable if none specified send no logs
            if s['channel']:
                embed = await self.create_log(message, scores)
                return await self.bot.get_channel(s['channel']).send(embed=embed)


    async def create_log(self, message, reasons):
        guild = await self.bot.fetch_guild(message.guild.id)
        tz = await self.get_timezone(guild.region)
        embed = discord.Embed(title=f"Message removed in #{message.channel.name}",
                              description=str(datetime.datetime.utcnow()) + " UTC")
        embed.add_field(name=f"Message:", value=f"{message.content}")
        embed.add_field(name=f"Author:", value=f"{message.author.name}")
        reason_string = ""

        for reason in reasons:
            reason_string += reason + "\n"
        embed.add_field(name=f"Reason:", value=f"{reason_string.title()}")
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

    async def get_timezone(self, region):
        regions = {'amsterdam': 0,
                   'frankfurt': '',
                   'hongkong': '',
                   'india': '',
                   'japan': '',
                   'london': '',
                   'russia': '',
                   'singapore': '',
                   'southafrica': '',
                   'brazil': '',
                   'eu_central': '',
                   'eu_west': '',
                   'sydney': '',
                   'us_central': '',
                   'us_east': '',
                   'us_south': '',
                   'us_west': '',
                   'vip_amsterdam': '',
                   'vip_us_east': '',
                   'vip_us_west': ''}
        if region not in regions:
            return False
        return regions[region]
        pass


def setup(bot):
    bot.add_cog(AutoMod(bot))
