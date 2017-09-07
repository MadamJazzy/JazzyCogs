import discord
from discord.ext import commands
from cogs.utils import checks
import aiohttp
import re
import traceback
import asyncio
from datetime import timedelta
import json


class bancheck:
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    @commands.cooldown(1, 5000, type=commands.BucketType.server)
    @commands.command(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def mban(self, ctx):
        """Bans all users on https://bans.discordlist.net.
        """
        server = ctx.message.server
        channel = ctx.message.channel
        me = server.me
        if not channel.permissions_for(me).ban_members:
            await self.bot.say("\U0000274c I don't have **ban_members** permissions.\nHow am i supposed to ban Hmmm?")
            return
        await self.bot.say('Please wait this will take a while \U0001f559')
        payload = {"token": "1PtZj1zNRL"}
        async with self.session.post('https://bans.discordlist.net/api', data=payload) as resp:
            oldlist = await resp.json()
            newlist = []
            for ban in oldlist:
                newlist.append(ban[0])
            server = ctx.message.server.id
            counter = 0
            for userid in newlist:
                try:
                    await self.bot.http.ban(userid, server)
                    counter += 1
                    await asyncio.sleep(5)
                except:
                    traceback.print_exc()
                    await self.bot.say('\U0000274c some kinda of error')
        await self.bot.say('You have banned \U0001f528 {} bad users\U0001f44c'.format(counter))

    @mban.error
    async def mban_error(self, error, ctx):
        if type(error) is commands.CommandOnCooldown:
            fmt = (str(error)).split()
            word = fmt[7].strip("s")
            time = float(word)
            timer = round(time, 0)
            tdelta = str(timedelta(seconds=int(timer))).lstrip("0").lstrip(":")
            await self.bot.say("You can ban again in `{}`".format(tdelta))

    @commands.command(pass_context=True)
    @checks.admin_or_permissions(ban_members=True)
    async def bancheck(self, ctx):
        """Checks users for people who appear on https://bans.discordlist.net"""
        payload = {"token": "1PtZj1zNRL"}
        async with self.session.post('https://bans.discordlist.net/api', data=payload) as resp:
            oldlist = await resp.json()
            newlist = []
            for ban in oldlist:
                newlist.append(ban[0])
        server = ctx.message.server
        print(newlist)
        names = []
        for r in server.members:
            if r.id in newlist:
                names.append(str(r))

        await self.bot.say(
            "**Found `{}` members out of `{}` bans**\n\nNames:```[{}]```".format(len(names), len(newlist),
                                                                                 ", ".join(names)))

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def munban(self, ctx):
        """Unban all users!"""
        server = ctx.message.server
        channel = ctx.message.channel
        me = server.me
        if not channel.permissions_for(me).ban_members:
            await self.bot.say("\U0000274c I don't have **ban_members** permissions.\nHow am i supposed to ban Hmmm?")
            return
        counter = 0
        await self.bot.say("just a sec")
        for user in await self.bot.get_bans(server):
            try:
                await self.bot.unban(server, user)
                counter += 1
                await asyncio.sleep(1.5)
            except:
                pass
                traceback.print_exc()

        await self.bot.say('You have unbanned \U0001f528 {} bad users\U0001f44c'.format(counter))


def setup(bot):
    bot.add_cog(bancheck(bot))