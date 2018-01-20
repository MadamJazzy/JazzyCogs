import discord
from discord.ext import commands
import aiohttp
import re
import os
from cogs.utils import checks
from __main__ import send_cmd_help
from .utils.dataIO import dataIO
import requests
URL = 'https://bans.discordlist.net/api'

class BanList():

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    def embed_maker(self, title, color, description, avatar):
        embed = discord.Embed(title=title, color=color, description=description)
        embed.set_thumbnail(url=avatar)
        return embed

    def payload(self, user):
        passthis = {
            'token': 'X9i69SJRQf',
            'userid': user,
            'version': 3,
        }
        return passthis

    def cleanurl(self, tag):
        re1 = '.*?'
        re2 = '((?:http|https)(?::\\/{2}[\\w]+)(?:[\\/|\\.]?)(?:[^\\s"]*))'
        rg = re.compile(re1 + re2, re.IGNORECASE | re.DOTALL)
        m = rg.search(tag)
        if m:
            theurl = m.group(1)
            return theurl

    async def lookup(self, user):
        resp = await self.session.get(URL, data=self.payload(user))
        final = await resp.json(content_type="text/html")
        resp.close()
        return final

    @commands.group()
    async def bancheck(self, ctx):
        'Checks for global bans on Discord.Services and DiscordList.net'
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @bancheck.command()
    async def user(self, ctx, user: discord.Member=None):
        'Check by username mention! [p]bancheck user @username'
        if (not user):
            user = ctx.author
        user1 = await self.bot.get_user_info(str(user.id))
        avatar = user1.avatar_url
        ds = requests.get('http://discord.services/api/ban/{}/'.format(user.id))
        try:
            name = ds.json()['ban']['name']
            userid = ds.json()['ban']['id']
            reason = ds.json()['ban']['reason']
            proof = ds.json()['ban']['proof']
            niceurl = '[Click Here]({})'.format(proof)
            description = '**Name:** {}\n**ID:** {}\n**Reason:** {}\n**Proof:** {}'.format(name, userid, reason, niceurl)
            await ctx.send(embed=self.embed_maker(':x: **Ban Found on Discord.Services!**', discord.Color.red(), description, avatar))
        except KeyError:
            await ctx.send(embed=self.embed_maker(':white_check_mark: Not listed on Discord.Services', 32768, None, avatar))
        try:
            final = await self.lookup(user.id)
        except ValueError:
            return await ctx.send(embed=self.embed_maker(':white_check_mark: Not listed on Discordlist.net ', 32768, None, avatar))
        name = final[1].replace('<Aspect>', '')
        userid = final[2]
        reason = final[3]
        proof = self.cleanurl(final[4])
        niceurl = '[Click Here]({})'.format(proof)
        description = '**Name:** {}\n**ID:** {}\n**Reason:** {}\n**Proof:** {}'.format(name, userid, reason, niceurl)
        await ctx.send(embed=self.embed_maker(':x: **Ban Found on Discordlist.net!** ', discord.Color.red(), description, avatar))

    @bancheck.command()
    async def id(self, ctx, id: str):
        'Check by UserID [p]bancheck id UserID'
        if (not id.isdigit()):
            await ctx.send('User ids only\nExample:`248294452307689473`')
            return
        try:
            user = await self.bot.get_user_info(id)
        except discord.errors.NotFound:
            await ctx.send('No user with the id `{}` found.'.format(id))
            return
        except:
            await ctx.send('❌ An error has occured.')
            return
        user1 = await self.bot.get_user_info(str(user.id))
        avatar = user1.avatar_url
        ds = requests.get('http://discord.services/api/ban/{}/'.format(user.id))
        try:
            name = ds.json()['ban']['name']
            userid = ds.json()['ban']['id']
            reason = ds.json()['ban']['reason']
            proof = ds.json()['ban']['proof']
            niceurl = '[Click Here]({})'.format(proof)
            description = '**Name:** {}\n**ID:** {}\n**Reason:** {}\n**Proof:** {}'.format(name, userid, reason, niceurl)
            await ctx.send(embed=self.embed_maker(':x: Ban Found on Discord.Services!', discord.Color.red(), description, avatar))
        except KeyError:
            await ctx.send(embed=self.embed_maker(':white_check_mark: Not listed on Discord.Services', 32768, None, avatar))
        try:
            final = await self.lookup(user.id)
        except ValueError:
            return await ctx.send(embed=self.embed_maker(':white_check_mark: Not listed on Discordlist.net ', 32768, None, avatar))
        name = final[1].replace('<Aspect>', '')
        userid = final[2]
        reason = final[3]
        proof = self.cleanurl(final[4])
        niceurl = '[Click Here]({})'.format(proof)
        description = '**Name:** {}\n**ID:** {}\n**Reason:** {}\n**Proof:** {}'.format(name, userid, reason, niceurl)
        await ctx.send(embed=self.embed_maker(':x: Ban Found on Discordlist.net!', discord.Color.red(), description, avatar))

    @commands.command()
    async def banlist(self, ctx):
        payload = {
            'token': 'Sb2gFUYIk0',
        }
        async with self.session.post('https://bans.discordlist.net/api', data=payload) as resp:
            oldlist = await resp.json(content_type="text/html")
            newlist = []
            for ban in oldlist:
                newlist.append(ban[0])
        guild = ctx.guild
        names = []
        for r in guild.members:
            if r.id in newlist:
                names.append('``{}`` -- ``{}`` \n'.format(str(r), str(r.id)))
        em = discord.Embed(description='**Found `{}` members out of `{}` Global Bans on DiscordList.net!**'.format(len(names), len(newlist)), colour=discord.Color.red())
        for r in guild.members:
            if r.id in newlist:
                names.append('``{}`` -- ``{}`` \n'.format(str(r), str(r.id)))
                em.add_field(name=r, value=r.id)
        embedperm = ctx.guild.me.permissions_in(ctx.channel).embed_links
        if embedperm is True:
            await ctx.send(embed=em)
        else:
            await ctx.send('I cannot display this data, I do not have Embed permissions in this channel. Please correct and run this command again!')
        async with self.session.get('http://discord.services/api/bans/') as resp:
            r = await resp.json()
            oldlist = r['bans']
            newlist = []
            for ban in oldlist:
                newlist.append(ban['id'])
        guild = ctx.guild
        names = []
        for r in guild.members:
            if r.id in newlist:
                names.append('``{}`` -- ``{}`` \n'.format(str(r), str(r.id)))
        em = discord.Embed(description='**Found `{}` members out of `{}` Global Bans on Discord.Services!**'.format(len(names), len(newlist)), colour=discord.Color.red())
        for r in guild.members:
            if r.id in newlist:
                names.append('``{}`` -- ``{}`` \n'.format(str(r), str(r.id)))
                em.add_field(name=r, value=r.id)
        embedperm = ctx.guild.me.permissions_in(ctx.channel).embed_links
        if embedperm is True:
            await ctx.send(embed=em)
        else:
            await ctx.send('I cannot display this data, I do not have Embed permissions in this channel. Please correct and run this command again!')

def setup(bot):
    n = BanList(bot)
    bot.add_cog(n)