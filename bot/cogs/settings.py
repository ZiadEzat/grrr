from discord.ext import commands
import discord
from .utils.db import *
from .utils import checks


class EnableDiable(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @checks.is_admin()
    async def disable(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Invalid disable command passed...", color=discord.Color.red())
            await ctx.send(embed=embed)

    @disable.group()
    async def joinlog(self, ctx):
        await updateSettings(ctx.guild.id, {"joinLog": {"enabled": False}})
        embed = discord.Embed(title="Done! :white_check_mark:", description="JoinLog module has been disabled!",
                              color=discord.Color.green())
        await ctx.send(embed=embed)

    @disable.group(aliases=['rr'])
    async def reactionroles(self, ctx):
        await updateSettings(ctx.guild.id, {"reactionRoles": {"enabled": False}})
        embed = discord.Embed(title="Done! :white_check_mark:", description="Reaction Roles module has been disabled!",
                              color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.group()
    @checks.is_admin()
    async def enable(self ,ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Invalid enabled command passed...", color=discord.Color.red())
            await ctx.send(embed=embed)

    @enable.group(aliases=['rr'])
    async def reactionroles(self, ctx):
        await updateSettings(ctx.guild.id, {"reactionRoles": {"enabled": True}})
        embed = discord.Embed(title="Done! :white_check_mark:", description="Reaction Roles module has been enabled!",
                              color=discord.Color.green())
        await ctx.send(embed=embed)

    @enable.group()
    async def joinlog(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            await ctx.send("```diff\n - Please specify the channel you want to enable this on\n```")
        await updateSettings(ctx.guild.id, {"joinLog": {"enabled": True, "join_log_channel_id": channel.id}})
        embed = discord.Embed(title="Done! :white_check_mark:", description="JoinLog module has been enabled!",
                              color=discord.Color.green())
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(EnableDiable(bot))
