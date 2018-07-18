import discord
from discord.ext import commands
import aiohttp
import re
import os
from cogs.utils import checks
from __main__ import send_cmd_help
from .utils.dataIO import dataIO
import requests

URL = "https://bans.discordlist.net/api"
URL2 = "https://api.ksoft.si/bans/info"

class BanList():
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)


    def embed_maker(self, title, color, description, avatar):
        embed=discord.Embed(title=title, color=color, description=description)
        embed.set_thumbnail(url=avatar)
        return embed

    def payload(self, user):
        passthis = {
        "token": "X9i69SJRQf",
        "userid": user,
        "version": 3}
        return passthis

    def cleanurl(self, tag):
        re1='.*?'
        re2='((?:http|https)(?::\\/{2}[\\w]+)(?:[\\/|\\.]?)(?:[^\\s"]*))'
        rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
        m = rg.search(tag)
        if m:
            theurl=m.group(1)
            return theurl

    async def lookup(self, user):
        resp = await aiohttp.post(URL, data=self.payload(user))
        final = await resp.json()
        resp.close()
        return final


    @commands.group(pass_context=True)
    async def banlist(self, ctx):
        """Checks for global bans on Discord.Services, DiscordList.net, AlertBot, and KSoft API!!"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @banlist.command(pass_context=True)
    async def user(self, ctx, user: discord.Member=None):
        """Check by username mention! | Usage: banlist user @username"""
        if not user:
            user = ctx.message.author
        user1 = await self.bot.get_user_info(str(user.id))
        avatar = user1.avatar_url
        #DSban Lookup
        ds = requests.get("http://discord.services/api/ban/{}/".format(user.id))
        try:
            name = user1
            userid = ds.json()["ban"]["id"]
            reason = ds.json()["ban"]["reason"]
            proof = ds.json()["ban"]["proof"]
            niceurl = "[Click Here]({})".format(proof)
            description = (
                """**Name:** {}\n**ID:** {}\n**Reason:** {}\n**Proof:** {}""".format(
                    name, userid, reason, niceurl))
            await self.bot.say(
                embed=self.embed_maker(":x: **Globally banned on Discord.Services!**", discord.Color.red(),
                                       description, ""))
        except KeyError:
            await self.bot.say(
                embed=self.embed_maker(":white_check_mark: Not listed on Discord.Services", 0x008000, None, ""))
        #AlertBot Lookup
        try:
            key = "c35ccd3cb3b99c3597c3e74c528e000b"
            ab = requests.get("http://generic-api.site/api/discordbans/?userid={}&key={}".format(user.id, key))
            abban = ab.json()[0]
            if abban["banned"] == "false":
                await self.bot.say(
                    embed=self.embed_maker(":white_check_mark: No ban found on AlertBot!", 0x008000, None, ""))
            else:
                name = user.name
                userid = user.id
                reason = abban["reason"]
                proof = "http://hubbot.io/alertbot/proofpics/{}".format((abban["image"]))
                niceurl = "[Click Here]({})".format(proof)
                description = (
                    """**Name:** {}\n**ID:** {}\n**Reason:** {}\n**Proof:** {}""".format(
                        name, userid, reason, niceurl))
                await self.bot.say(embed=self.embed_maker(":x: **Globally banned on AlertBot!** ", discord.Color.red(),
                                                          description, ""))
        except KeyError:
            pass

        #Equalizer Bot lookup
        try:
            myToken = 'cf1af2a4bb8d2e22af790b66c179e49a2c733d12'
            equrl = 'https://api.ksoft.si/bans/info'
            head = {'Authorization': 'token {}'.format(myToken)}
            params = {"user": user.id}
            eq = requests.get(equrl, headers=head, params=params)
            final = eq.json()
            userid = final["id"]
            name = final["name"] + ["discriminator"]
            reason = final["reason"]
            proof = self.cleanurl(final["proof"])
            niceurl = "[Click Here]({})".format(proof)
            description = (
                """**Name:** {}\n**ID:** {}\n**Reason:** {}\n**Proof:** {}""".format(
                    name, userid, reason, niceurl))
            await self.bot.say(embed=self.embed_maker(":x: **Globally banned on Equalizer Bot!** ", discord.Color.red(),
                                                      description, ""))
        except KeyError:
            await self.bot.say(
                embed=self.embed_maker(":white_check_mark: No ban found on Equalizer Bot!", 0x008000, None, ""))

        #Dbans lookup
#        try:
#            final = await self.lookup(user.id)
#        except ValueError:
#            return await self.bot.say(embed=self.embed_maker(":white_check_mark: Not listed on Discordlist.net ",
#                                                             0x008000, None, ""))
#        name = (final[1].replace("<Aspect>", ""))
#        userid = final[2]
#        reason = final[3]
#        proof = self.cleanurl(final[4])
#        niceurl = "[Click Here]({})".format(proof)
#        description = (
#            """**Name:** {}\n**ID:** {}\n**Reason:** {}\n**Proof:** {}""".format(
#                name, userid, reason, niceurl))
#        await self.bot.say(embed=self.embed_maker(":x: **Globally banned on DiscordList.net** ", discord.Color.red(),
#                                                  description, ""))

    @banlist.command(pass_context=True)
    async def id(self, ctx, id: str):
        """Check by user ID | Usage: banlist id 123456789123"""
        if (not id.isdigit()):
            await self.bot.say('User ids only\nExample:`248294452307689473`')
            return
        try:
            user = await self.bot.get_user_info(id)
        except discord.errors.NotFound:
            await self.bot.say('No user with the id `{}` found.'.format(id))
            return
        except:
            await self.bot.say('❌ An error has occured.')
            return
        user1 = await self.bot.get_user_info(str(user.id))
        avatar = user1.avatar_url
        ds = requests.get("http://discord.services/api/ban/{}/".format(user.id))
        try:
            name = user1
            userid = ds.json()["ban"]["id"]
            reason = ds.json()["ban"]["reason"]
            proof = ds.json()["ban"]["proof"]
            niceurl = "[Click Here]({})".format(proof)
            description = (
                """**Name:** {}\n**ID:** {}\n**Reason:** {}\n**Proof:** {}""".format(
                    name, userid, reason, niceurl))
            await self.bot.say(
                embed=self.embed_maker(":x: Ban Found on Discord.Services!", discord.Color.red(),
                                       description, ""))
        except KeyError:
            await self.bot.say(
                embed=self.embed_maker(":white_check_mark: Not listed on Discord.Services", 0x008000, None, ""))

        try:
            key = "c35ccd3cb3b99c3597c3e74c528e000b"
            ab = requests.get("http://generic-api.site/api/discordbans/?userid={}&key={}".format(user.id, key))
            abban = ab.json()[0]
            if abban["banned"] == "false":
                await self.bot.say(
                    embed=self.embed_maker(":white_check_mark: No ban found on AlertBot!", 0x008000, None, ""))
            else:
                name = user.name
                userid = user.id
                reason = abban["reason"]
                proof = "http://hubbot.io/alertbot/proofpics/{}".format((abban["image"]))
                niceurl = "[Click Here]({})".format(proof)
                description = (
                    """**Name:** {}\n**ID:** {}\n**Reason:** {}\n**Proof:** {}""".format(
                        name, userid, reason, niceurl))
                await self.bot.say(embed=self.embed_maker(":x: **Ban Found on AlertBot!** ", discord.Color.red(),
                                                          description, ""))
        except KeyError:
            await self.bot.say("Key Error")

        #Equalizer Bot lookup
        try:
            myToken = 'cf1af2a4bb8d2e22af790b66c179e49a2c733d12'
            equrl = 'https://api.ksoft.si/bans/info'
            head = {'Authorization': 'token {}'.format(myToken)}
            params = {"user": user.id}
            eq = requests.get(equrl, headers=head, params=params)
            final = eq.json()
            userid = final["id"]
            name = '{}#{}'.format(final['name'], final['discriminator'])
            reason = final["reason"]
            proof = self.cleanurl(final["proof"])
            niceurl = "[Click Here]({})".format(proof)
            description = (
                """**Name:** {}\n**ID:** {}\n**Reason:** {}\n**Proof:** {}""".format(
                    name, userid, reason, niceurl))
            await self.bot.say(embed=self.embed_maker(":x: **Globally banned on Ksoft Banlist!** ", discord.Color.red(),
                                                      description, ""))
        except KeyError:
            await self.bot.say(
                embed=self.embed_maker(":white_check_mark: No ban found on Equalizer Bot!", 0x008000, None, ""))

#        try:
#            final = await self.lookup(user.id)
#        except ValueError:
#            return await self.bot.say(
#                embed=self.embed_maker(":white_check_mark: Not listed on Discordlist.net ", 0x008000, None, ""))
#        name = (final[1].replace("<Aspect>", ""))
#        userid = final[2]
#        reason = final[3]
#        proof = self.cleanurl(final[4])
#        niceurl = "[Click Here]({})".format(proof)
#        description = (
#            """**Name:** {}\n**ID:** {}\n**Reason:** {}\n**Proof:** {}""".format(
#                name, userid, reason, niceurl))
#        await self.bot.say(
#            embed=self.embed_maker(":x: Ban Found on Discordlist.net!",discord.Color.red(),
#                                   description, avatar))
    @banlist.command(pass_context=True)
    async def all(self, ctx):
        """Scan the **entire** server for banned users!"""
        payload = {"token": "Sb2gFUYIk0"}
        myToken = 'cf1af2a4bb8d2e22af790b66c179e49a2c733d12'
        equrl = 'https://api.ksoft.si/bans/list'
        head = {'Authorization': 'token {}'.format(myToken)}
        params = {"per_page": 5000}
        green = discord.Color.green()
        red = discord.Color.red()
#        async with self.session.post('https://bans.discordlist.net/api', data=payload) as resp:
#            oldlist = await resp.json()
#            newlist = []
#            for ban in oldlist:
#                newlist.append(ban[0])
#        server = ctx.message.server
#        names = []
#        for r in server.members:
#            if r.id in newlist:
#                names.append("``{}`` -- ``{}`` \n".format(str(r), str(r.id),))
#        if len(names) is not 0:
#            em = discord.Embed(title="DiscordList.net Ban List", description="**Found {} bad users!**".format(len(names)), color=red)
#        else:
#            em = discord.Embed(title="DiscordList.net Ban List", description="**NO bad users found!**", color=green)
#        if len(names) is not 0:
#            for r in server.members:
#                if r.id in newlist:
#                    names.append("``{}`` -- ``{}`` \n".format(str(r), str(r.id)))
#                    em.add_field(name=" {} ".format(r), value="   {}   ".format(r.id))
#        embedperm = ctx.message.server.me.permissions_in(ctx.message.channel).embed_links
#        if embedperm is True:
#            await self.bot.say(embed=em)
#        else:
#            await self.bot.say("I cannot display this data, I do not have Embed permissions in this channel. "
#                               "Please correct and run this command again!")

        async with self.session.get('http://discord.services/api/bans/') as resp:
            r = await resp.json()
            oldlist = r["bans"]
            newlist = []
            for ban in oldlist:
                newlist.append(ban["id"])
        server = ctx.message.server
        names = []
        for r in server.members:
            if r.id in newlist:
                names.append("``{}`` -- ``{}`` \n".format(str(r), str(r.id),))
        if len(names) is not 0:
            em = discord.Embed(title="Discord.Services Ban List", description="**Found {} bad users!**".format(len(names)), color=red)
        else:
            em = discord.Embed(title="Discord.Services Ban List", description="**NO bad users found!**", color=green)
        if len(names) is not 0:
            for r in server.members:
                if r.id in newlist:
                    names.append("``{}`` -- ``{}`` \n".format(str(r), str(r.id)))
                    em.add_field(name=" {} ".format(r), value="   {}   ".format(r.id))
        embedperm = ctx.message.server.me.permissions_in(ctx.message.channel).embed_links
        if embedperm is True:
            await self.bot.say(embed=em)
        else:
            await self.bot.say("I cannot display this data, I do not have Embed permissions in this channel. "
                               "Please correct and run this command again!")


        async with self.session.get(equrl, headers=head, params=params) as resp:
            r = await resp.json()
            oldlist = r['data']
            newlist = []
            for ban in oldlist:
                newlist.append(ban['id'])
        server = ctx.message.server
        names = []
        for r in server.members:
            if r.id in newlist:
                names.append("``{}`` -- ``{}`` \n".format(str(r), str(r.id),))
        if len(names) is not 0:
            em = discord.Embed(title="KSoft API Ban List", description="**Found {} bad users!** ".format(len(names)), color=red)
        else:
            em = discord.Embed(title="KSoft API Ban List", description="**NO bad users Found!** ", color=green)
        if len(names) is not 0:
            for r in server.members:
                if r.id in newlist:
                    names.append("``{}`` -- ``{}`` \n".format(str(r), str(r.id)))
                    em.add_field(name=" {} ".format(r), value="   {}   ".format(r.id))
        embedperm = ctx.message.server.me.permissions_in(ctx.message.channel).embed_links
        if embedperm is True:
            await self.bot.say(embed=em)
        else:
            await self.bot.say("I cannot display this data, I do not have Embed permissions in this channel. "
                               "Please correct and run this command again!")


def setup(bot):
    n = BanList(bot)
    bot.add_cog(n)
