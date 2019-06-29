from discord.ext import commands

from .utils.db import *


def Enabled():
    async def predicate(ctx):
        s = await ctx.cog.getSettings(ctx.guild.id)
        if s['enabled'] == True:
            return True
        else:
            raise False


class reactionRoles(commands.Cog):
    """Easy to set up reaction roles feature"""

    def __init__(self, bot):
        self.bot = bot

        self.default_emojis = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣',
                               '🔟', '🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮',
                               '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', '🇵', '🇶', '🇷', '🇸',
                               '🇹', '🇺', '🇻', '🇼', '🇽', '🇾', '🇿']

    # async def updateQ(self,q):
    # 	await self.db['queues'].update_one({'server_id':q['server_id'],'channel_id':q['channel_id']},{'$set':q},upsert=True)

    # self.updateSettings(ctx.guild.id,message.channel.id,message.id,d)
    async def updateRR(self, gid, cid, mid, d):
        await db['reactionRoles'].update_one({'server_id': gid, 'channel_id': cid, 'message_id': mid}, {'$set': d},
                                             upsert=True)

    async def getRR(self, gid, cid, mid):
        d = await db['reactionRoles'].find_one({'server_id': gid, 'channel_id': cid, 'message_id': mid})
        return d

    async def getSettings(self, server_id):
        return await getSettings(server_id, cog="reactionRoles")

    @commands.command()
    async def postRRMessage(self, ctx, category: str, exclusive: bool = False, *emojis):
        """Post a message users can react to in order to get a role, syntax: !postRRMessage <category_name> <optional:is_exclusive> <optional:custom_emojis> """

        s = await ctx.cog.getSettings(ctx.guild.id)
        if s['enabled'] == True:
            return True

        d = {}
        d['emojis'] = emojis
        d['category'] = category
        d['reactions'] = {}
        d['exclusive'] = exclusive

        categoryRoles = get_category_roles(ctx.guild, d['category'])

        emojis = self.get_emojis(d['emojis'])

        msg, d = self.make_rr_message(ctx.guild, d)
        message = await ctx.send(msg)
        for e in d['reactions'].keys():
            await message.add_reaction(e)

        await self.updateRR(ctx.guild.id, message.channel.id, message.id, d)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # g = self.bot.get_guild(payload.guild_id)
        # c = g.get_channel(payload.channel_id)
        # m = await c.fetch_message(payload.message_id)

        # user = g.get_member(payload.user_id)
        # emoji = str(payload.emoji)

        g, c, m, user, emoji = await self.parse_payload(payload)

        if user.bot:
            return

        s = await self.getSettings(g.id)

        if not s['enabled']:
            return

        d = await self.getRR(g.id, c.id, m.id)

        if d == None:
            return

        rid = d['reactions'].get(emoji, None)

        if rid == None:
            return

        r = [r for r in g.roles if r.id == rid][0]  # check role exists blah blah blah
        await user.add_roles(r)

        if d['exclusive']:

            categoryRoles = [d['reactions'][e] for e in d['reactions'].keys()]
            intersect = set(categoryRoles) & set([rol.id for rol in user.roles])
            intersect.discard(r.id)
            if len(intersect) > 0:
                roles = [x for x in g.roles if ((x.id in intersect) and r != x)]
                for role in roles:
                    await user.remove_roles(role)
                    for react in m.reactions:
                        if emoji != react.emoji:
                            await m.remove_reaction(react, user)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        g, c, m, user, emoji = await self.parse_payload(payload)

        if user.bot:
            return

        s = await self.getSettings(g.id)

        if not s['enabled']:
            return

        d = await self.getRR(g.id, c.id, m.id)

        if d == None:
            return

        rid = d['reactions'].get(emoji, None)

        if rid == None:
            return

        r = [r for r in g.roles if r.id == rid][0]  # check role exists blah blah blah
        await user.remove_roles(r)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):

        guild = before.guild
        cursor = self.db['reactionRoles'].find({'server_id': guild.id})

        async for d in cursor:
            # el rol estaba en una cat, pero ahora no -> remake
            # el role no estaba, pero ahora si -> remake
            was = is_in_category(guild, before, d['category'])
            isnow = is_in_category(guild, after, d['category'])

            if was or isnow:
                content, d = self.make_rr_message(guild, d)
                channel = guild.get_channel(d['channel_id'])
                message = await channel.fetch_message(d['message_id'])

                await message.edit(content=content)

                emojis_in_reaction = [re.emoji for re in message.reactions]
                emojis = self.get_emojis(d['emojis'])

                for reaction in message.reactions:
                    if reaction.emoji not in content:
                        async for user in reaction.users():
                            await message.remove_reaction(reaction, user)

                for emoji in emojis:
                    if emoji in content and not emoji in emojis_in_reaction:
                        await message.add_reaction(emoji)

                await self.updateRR(guild.id, message.channel.id, message.id, d)

    async def parse_payload(self, payload):
        g = self.bot.get_guild(payload.guild_id)
        c = g.get_channel(payload.channel_id)
        m = await c.fetch_message(payload.message_id)

        user = g.get_member(payload.user_id)
        emoji = str(payload.emoji)
        return g, c, m, user, emoji

    def make_rr_message(self, guild, d):
        categoryRoles = get_category_roles(guild, d['category'])
        emojis = self.get_emojis(d['emojis'])
        if len(categoryRoles) > len(emojis):
            raise generic(message="Not enough emojis :x:")  # test this shit

        i = 0
        msg = ''
        for r in categoryRoles:
            emoji = emojis[i]
            msg += f"{emoji} {fake_mention(r)} \n \n"
            i += 1
            d['reactions'][emoji] = r.id

        return msg, d

    def get_emojis(self, customEmojis):
        emojis = customEmojis
        if emojis == None:
            emojis = self.default_emojis
        else:
            seq = list(emojis) + self.default_emojis
            seen = set()
            seen_add = seen.add
            emojis = [x for x in seq if not (x in seen or seen_add(x))]

        return emojis


def fake_mention(role):
    return f"<@&{role.id}>"


def is_in_category(guild, r, category):
    topSeparator = [r for r in guild.roles if r.name == f"<{category}>"][0]
    bottomSeparator = [r for r in guild.roles if r.name == f"</{category}>"][0]
    return (r < topSeparator and r > bottomSeparator)


def get_category_roles(guild, category):
    topSeparator = None
    bottomSeparator = None
    try:
        topSeparator = [r for r in guild.roles if r.name == f"<{category}>"][0]
        bottomSeparator = [r for r in guild.roles if r.name == f"</{category}>"][0]
    except Exception as e:
        print("ERROR GETTING CATEGORY ROLES")
        print(e)

    if not (topSeparator != None and bottomSeparator != None and topSeparator > bottomSeparator):
        print("NO CAT ROLES")
        return None

    return list(reversed([r for r in guild.roles if (r < topSeparator and r > bottomSeparator)]))


def setup(bot):
    bot.add_cog(reactionRoles(bot))
