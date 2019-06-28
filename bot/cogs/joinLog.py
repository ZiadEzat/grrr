from discord.ext import commands
from discord.ext.commands import bot
import discord
import asyncio
import timeago
import datetime
# import utils.cog
#on_guild_join recrawl
from .utils.db import *


class joinLog(commands.Cog):
	
	def __init__(self,bot):
		self.bot = bot
		self.invites = {}
		self.crawler = self.bot.loop.create_task(self.crawl_invites())


	async def getSettings(self,server_id):
		return await getSettings(server_id,cog="joinLog")

	async def crawl_invites(self):
		for guild in self.bot.guilds:
			try:
				guild_invites = {}
				invites = await guild.invites()
				for invite in invites:
					guild_invites[invite.code] = invite
				self.invites[guild] = guild_invites
			except discord.errors.Forbidden:
				pass


	async def find_possible_invites(self,guild):
		i = 1
		while i < 11:
			new = await guild.invites()
			res = []
			for invite in new:
				try:
					old_uses = self.invites[guild][invite.code].uses
				except KeyError:
					self.invites[guild][invite.code] = invite
					if invite.uses >= 1:
						res.append(invite)
					continue
				new_uses = invite.uses
				if old_uses < new_uses :
					self.invites[guild][invite.code] = invite
					res.append(invite)

			if res == []:
				await asyncio.sleep(3)
				i+=1
			else:
				break
		return res

	@commands.Cog.listener()
	async def on_member_join(self,member):
		s = await self.getSettings(member.guild.id)
		if not s['enabled']:
			return
		if 'join_log_channel_id' in s.keys():
			possible_invites = await self.find_possible_invites(member.guild)
			channel = member.guild.get_channel(s['join_log_channel_id'])
			nothing = "** **"
			e = discord.Embed()

			e.colour = discord.Colour.blue()
			e.title = "Member Joined!"
			#e.set_author(name=nothing,icon_url=member.avatar_url)
			e.add_field(name="Name",value=str(member))
			e.add_field(name="ID:",value=member.id)
			if len(possible_invites) == 1:
				e.add_field(name="Acount created",value=timeago.format(member.created_at, datetime.datetime.now()))
				e.add_field(name="Invite used",value=possible_invites[0].url,inline=True)
				e.add_field(name="Invite created by",value=str(possible_invites[0].inviter),inline=True)
				e.add_field(name="Number of uses",value=str(possible_invites[0].uses),inline=True)

				
			elif len(possible_invites) > 1:
				e.add_field(name="Possible invites used:",value=nothing,inline=False)
				for i in possible_invites:
					e.add_field(name=nothing,value=i.url,inline=False)
			else:
				e.add_field(name="Invite used could not be detected",value=nothing,inline=False)

			await channel.send(embed=e)

def setup(bot):
	bot.add_cog(joinLog(bot))
