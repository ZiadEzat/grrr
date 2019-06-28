import discord
from discord.ext import commands

from .utils.db import *


class settings(commands.Cog):
    """Configure the bot's modules"""
    def __init__(self, bot):
        self.bot = bot
        self.valid_cogs = ["autoMod","joinLog","reactionRoles"]


    @commands.command()
    async def disable(self, ctx, cog:str):
        """Disable a module, syntax: !disable <moduleName>"""
       
        loaded_cogs = self.get_loaded_cogs()

        if cog not in loaded_cogs:
            await self.cogDoesNotExist(ctx.channel)
            return
        
        
        await updateSettings(ctx.guild.id, {cog: {"enabled": False}})
        await ctx.send("done :thumbsup:")


    @commands.command()
    async def enable(self, ctx, cog: str, channel: discord.TextChannel = None):
        """Enable a module, syntax: !enable <moduleName> <optional:logging_channel>"""

        loaded_cogs = self.get_loaded_cogs()
        if cog not in loaded_cogs:
            await self.cogDoesNotExist(ctx.channel)
            return
        if channel is None:
            await updateSettings(ctx.guild.id, {cog: {"enabled": True, "channel": False}})
            await ctx.send("done :thumbsup:")
        else:
            await updateSettings(ctx.guild.id, {cog: {"enabled": True, "channel": channel.id}})
            await ctx.send(f"done :thumbsup: {cog} logging will be sent to {channel.name}")


    async def cogDoesNotExist(self,channel): #naje tgus oretty plz
        loaded_cogs = self.get_loaded_cogs()

        msg = "Invalid module name, valid ones are: \n"
        for cog in loaded_cogs:
            msg += cog + '\n'

        await channel.send(msg)

    def get_loaded_cogs(self):
        res = [name for name,cog in self.bot.cogs.items() if name in self.valid_cogs]
        return res


    # @commands.group()
    # @checks.is_admin()
    # async def disable(self, ctx):
    #     if ctx.invoked_subcommand is None:
    #         embed = discord.Embed(title="Invalid disable command passed...", color=discord.Color.red())
    #         await ctx.send(embed=embed)

    # @disable.group()
    # async def joinlog(self, ctx):
    #     await updateSettings(ctx.guild.id, {"joinLog": {"enabled": False}})
    #     embed = discord.Embed(title="Done! :white_check_mark:", description="JoinLog module has been disabled!",
    #                           color=discord.Color.green())
    #     await ctx.send(embed=embed)

    # @disable.group(aliases=['rr'])
    # async def reactionroles(self, ctx):
    #     await updateSettings(ctx.guild.id, {"reactionRoles": {"enabled": False}})
    #     embed = discord.Embed(title="Done! :white_check_mark:", description="Reaction Roles module has been disabled!",
    #                           color=discord.Color.green())
    #     await ctx.send(embed=embed)

    # @commands.group()
    # @checks.is_admin()
    # async def enable(self ,ctx):
    #     if ctx.invoked_subcommand is None:
    #         embed = discord.Embed(title="Invalid enabled command passed...", color=discord.Color.red())
    #         await ctx.send(embed=embed)

    # @enable.group(aliases=['rr'])
    # async def reactionroles(self, ctx):
    #     await updateSettings(ctx.guild.id, {"reactionRoles": {"enabled": True}})
    #     embed = discord.Embed(title="Done! :white_check_mark:", description="Reaction Roles module has been enabled!",
    #                           color=discord.Color.green())
    #     await ctx.send(embed=embed)

    # @enable.group()
    # async def joinlog(self, ctx, channel: discord.TextChannel = None):
    #     if channel is None:
    #         await ctx.send("```diff\n - Please specify the channel you want to enable this on\n```")
    #     await updateSettings(ctx.guild.id, {"joinLog": {"enabled": True, "join_log_channel_id": channel.id}})
    #     embed = discord.Embed(title="Done! :white_check_mark:", description="JoinLog module has been enabled!",
    #                           color=discord.Color.green())
    #     await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(settings(bot))
