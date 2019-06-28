

from discord.ext import commands
from discord.ext.commands import bot
import discord

from .utils.db import *

class Help(commands.Cog):
	
	def __init__(self,bot):
		self.bot = bot
		bot.remove_command('help')


	@commands.command(aliases=["help"])
	async def _help(self,ctx,cog=None):

			e = discord.Embed()
			e.colour = discord.Colour.blue()
			if cog == None:
				
				
				e.title = "RAM Modules"
				e.add_field(name="autoMod",value="Automatically filter (some) inapropiate chat messages leveraging the power of AI",inline=False)
				e.add_field(name="joinLog",value="Get useful intel on who joins your guild, including invite link used and account's age",inline=False)
				e.add_field(name="reactionRoles",value="The popular feature, made easy",inline=False)
				e.description = "use !help module_name to learn how to use each module"

			elif cog == "autoMod":
				
				e.title = "autoMod commands"
				e.add_field(name="!enable autoMod <optional: log_channel>",value="Enables the feature and sets a logging channel if specified")

			elif cog == "joinLog":
				e.title = "joinLog commands"
				e.add_field(name="!enable joinLog <log_channel>",value="Enables the feature to log new users info in the specifed channel")
			
			elif cog == "reactionRoles":
				e.title = "reactionRoles commands"
				e.add_field(name="!postRRMessage <category_name> <optional:exclusive?>",value="""
				
				How to use:

				Step 1: Pick a name for your role category, in this example, i'll use the name "colors"
				Step 2: Create a top separator role, named <category_name>, in this case "<colors>"
				Step 3: Create a bottom separator role, named </category_name>, in this case "</colors>"
				Step 4: Make sure the top sepparator role is above the bottom separator role in your role hierarchy
				step 5: Put as many roles as you want between this 2 roles, for people to get with reactions
				step 6: Do !postRRMessage category_name and the bot will post the message people can react to

				In this example, it would be !postRRMessage colors 

				If you want users to only be able to get one of the roles in the category, add the true parameter, ie:

				!postRRMessage colors True


				""")
			
			else:
				await ctx.send(f"No module named {cog}")
				return
			await ctx.send(embed=e)

						


def setup(bot):
	bot.add_cog(Help(bot))
