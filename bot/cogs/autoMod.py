from discord.ext import commands
from discord.ext.commands import bot

from .utils.db import *

import requests
import json


class autoMod(commands.Cog):
	
	def __init__(self,bot):
		self.bot = bot
		self.payload = {'key': bot.config['perspective_key']}
		
		self.headers = {'Content-Type': 'application/json'}
		self.treshold = 0.9
		self.numberOfFiltersAboveTresholdToFilter = 2
		self.debug = True

	async def getSettings(self,server_id):
		return await getSettings(server_id,cog="autoMod")

	@commands.Cog.listener()
	async def on_message(self,message):
		s = await getSettings(message.guild.id)
		
		if not s['enabled'] or message.author.bot:
			return
	   
		response = self.get_toxicity(message.content)

		response = response['attributeScores']

		msg = "String: " + message.content + "\n"

		scores = [ k for k,v in response.items()  if v['summaryScore']['value'] >= self.treshold ]

		if self.debug:
			for k,v in response.items():
				
				msg += f"{k} = {v['summaryScore']['value']} \n"
			await message.channel.send(msg)

		if len(scores) >= self.numberOfFiltersAboveTresholdToFilter:
			print(scores)
			await message.delete()
			return



		

		
		

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

