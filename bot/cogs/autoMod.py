import datetime
import json
import re

import discord
import requests
from discord.ext import commands

from .utils.db import *


class autoMod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.payload = {'key': bot.config['perspective_key']}

        self.headers = {'Content-Type': 'application/json'}
        self.treshold = 0.85
        self.numberOfFiltersAboveTresholdToFilter = 2
        self.debug = False

    async def countEmojis(self, message: discord.Message):
        count = len(re.findall("(\:[a-z_1-9A-Z]+\:)", message.content))  # custom emojis
        return count

    async def getSettings(self, server_id):
        return await getSettings(server_id, cog="autoMod")

    @commands.Cog.listener()
    async def on_message(self, message):
        s = await self.getSettings(message.guild.id)
        if not s['enabled'] or message.author.bot:
            return
        if await self.countEmojis(message) >= 3:
            await message.delete()
            await message.channel.send("please do not spam emojis")

        thing = message.content
        thing = str(thing).replace('_', ' ')
        response = self.get_toxicity(thing)
        response = response['attributeScores']
        msg = "String: " + message.content + "\n"
        scores = [k for k, v in response.items() if v['summaryScore']['value'] >= self.treshold]
        if self.debug:
            for k, v in response.items():
                msg += f"{k} = {v['summaryScore']['value']} \n"
            await message.channel.send(msg.title().replace('_', ' '))
        if len(scores) >= self.numberOfFiltersAboveTresholdToFilter:
            await message.delete()
            embed = await self.create_log(message, scores)
            # TODO: Send log messages to log channel specified on emable if none specified send no logs

            if s['channel']:
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
        embed.add_field(name=f"Reason:", value=f"{reason_string.title().replace('_', ' ')}")
        return embed

    def get_toxicity(self, comment, language='en'):
        languages = ['en', 'fr', 'es']
        if language not in languages:
            raise Exception("Invalid Language for toxicity report")
        data = {'comment': {'text': comment},
                'languages': [language],
                'requestedAttributes': {
                    'TOXICITY': {},
                    "THREAT": {},
                    "INSULT": {},
                    "PROFANITY": {},
                    "SEXUALLY_EXPLICIT": {}
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
    bot.add_cog(autoMod(bot))
