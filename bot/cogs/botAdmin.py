from discord.ext import commands
import discord
import re
from loguru import logger
from .utils import checks # This will say error in most IDSs, Ignore it
from .utils.commentAnalyzer import Predictor
import git


class CommonSpam(commands.Cog):
    """
    Fights against common spam that can plague discord servers
    """
    def __init__(self, bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     number_of_emojis = await self.countEmojis(message)
    #     if number_of_emojis >= 3:
    #         await message.delete()
    #         channel = await message.author.create_dm()
    #         await channel.send("Please do not spam")
    #     nn_results = await self.run_message_through_nn(message=message)
    #     logger.info(f'{message.content}: probability of profanity {float(nn_results[0])}')
    #
    #     if nn_results:
    #         await message.delete()
    #         channel = await message.author.create_dm()
    #         await channel.send("watch your language please")

    @commands.command()
    async def gitpull(self, ctx):
        git_dir = "./"
        try:
            g = git.cmd.Git(git_dir)
            g.pull()
            embed = discord.Embed(title="Successfully pulled from repository", color=0x00df00)
            await ctx.send(embed=embed)
        except Exception as e:
            errno, strerror = e.args
            embed = discord.Embed(title="Command Error!",
                                  description=f"Git Pull Error: {errno} - {strerror}",
                                  color=0xff0007)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CommonSpam(bot))
