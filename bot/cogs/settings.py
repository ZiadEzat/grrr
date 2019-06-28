from discord.ext import commands
from discord.ext.commands import bot
import discord
import asyncio
import timeago
import datetime
# import utils.cog
#on_guild_join recrawl
from .utils.db import *


class EnableDiable(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group()
    async def disable(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Invalid disable command passed...", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.group()
    async def enable(self ,ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Invalid enabled command passed...", color=discord.Color.red())
            await ctx.send(embed=embed)

    @enable.group()
    async def joinlog(self, ctx, channel: discord.TextChannel):
        await updateSettings(ctx.guild.id, {"joinLog": {"enabled": True, "join_log_channel_id": channel.id}})
        embed = discord.Embed(title="Done! :white_check_mark:", description="JoinLog module has been enabled!", color=discord.Color.green())
        await ctx.send(embed=embed)

    @disable.group()
    async def joinlog(self, ctx):
        await updateSettings(ctx.guild.id, {"joinLog": {"enabled": False}})
        embed = discord.Embed(title="Done! :white_check_mark:", description="JoinLog module has been disabled!", color=discord.Color.green())
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(EnableDiable(bot))
