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
        self._last_member = None

    async def countEmojis(self, message: discord.Message):
        count = len(re.findall("(\:[a-z_1-9A-Z]+\:)", message.content)) # custom emojis
        if count == 0: # Test for Unicode Emojis
            count = len(re.findall('(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|'
                                   '\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])', message.content))
        return count

    async def run_message_through_nn(self, message):
        """

        :param message:
        :return:
        """

        # return predict_prob([f'{message}'])
        pred = Predictor()
        return pred.get_toxicity(self, message)
        pass

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     number_of_emojis = await self.countEmojis(message)
    #     if number_of_emojis >= 3:
    #         await message.delete()
    #         channel = await message.author.create_dm()
    #         await channel.send("Please do not spam")
    #     nn_results = await self.run_message_through_nn(message=message.content)
    #     logger.info(f'{message.content}: probability of profanity {float(nn_results[0])}')
    #
    #     if float(nn_results[0]) > 0.65:
    #         await message.delete()
    #         channel = await message.author.create_dm()
    #         await channel.send("watch your language please")
    @commands.Cog.listener()
    async def on_message(self, message):

        if not message.author.bot:
            # t = self.predictor.get_toxicity(message.content)
            pred = Predictor()
            t = pred.get_toxicity(message.content)
            d = t['attributeScores']

            msg = ""

            for k, v in d.items():
                print(v)
                msg += f"{k} = {v['summaryScore']['value']} \n"

            # toxicity = t['attributeScores']['TOXICITY']['summaryScore']['value']
            # severe_toxicity = t['attributeScores']['SEVERE_TOXICITY']['summaryScore']['value']
            # ltr = t['attributeScores']['LIKELY_TO_REJECT']['summaryScore']['value']
            # spam = t['attributeScores']['SPAM']['summaryScore']['value']
            await message.channel.send(msg)



    @commands.command()
    @checks.is_admin()
    async def commonspam(self, ctx, setting = None):
        """
        Turn on or off the command spam checks
        :param ctx:
        :param setting: on or off
        :return:
        """
        if setting is None:
            await ctx.send("Please specify a setting! (on | off)")
        else:
            if setting.lower() == "on" or setting.lower() == "off":
                await ctx.send("Setting is now on")
                pass
            else:
                await ctx.send("Please specify a *correct* setting! (on | off)")

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
