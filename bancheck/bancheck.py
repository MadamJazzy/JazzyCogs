import discord
from discord.ext import commands
from requests import post, get
import json

from cogs.utils.checks import *


class DiscordBans:
    """Uses discordlist.net to check and list gloabal bans"""
    version = 1
    url = "https://raw.githubusercontent.com/Bluscream/ASCII/master/cogs/discordbans.json"

    class author(discord.ClientUser):
        name = "Jazzibell"
        discriminator = "7630"
        id = 209219778206760961
        email = ""

    # Cog Variables
    token = 'rnRKaAhkVX'
    imgur_clientid = 'aa3bde928fe4e09'

    def __init__(self, bot):
        self.bot = bot
        self.discordbans = json.loads(post('https://bans.discordlist.net/listing', data=[('token', self.token)]).text)[
            "data"]

    def banned(self, uid):
        if len(self.discordbans) > 0:
            for ban in self.discordbans:
                if str(uid) == ban[1]:
                    return ban
            return False

    @commands.command()
    async def bancheck(self, ctx, uid: int = None, reload: bool = True):
        """bancheck [userid] will list if and why a user was banned!"""
        await ctx.message.delete()
        if not uid: uid = self.bot.user.id
        if reload: self.discordbans = \
        json.loads(post('https://bans.discordlist.net/listing', data=[('token', self.token)]).text)["data"]
        embed = discord.Embed(description='\ðŸ”¨ **Global Ban Lookup for** <@{}>'.format(uid),
                              colour=discord.Color.green())
        _gban = self.banned(uid)
        if _gban is not None:
            if not _gban:
                embed.description = embed.description + '\n\nNot banned \âœ…'
            else:
                embed.add_field(name=':hammer: Banned', value='Yes \âŒ')
                embed.add_field(name=':pencil2: Name', value='`{}`'.format(_gban[0]))
                embed.add_field(name=':card_index: ID', value=_gban[1])
                embed.add_field(name=':notepad_spiral: Reason', value='``` {} ```'.format(_gban[2]))
                proof = _gban[3].replace('<a href="', '').replace('">Proof</a>', '')
                if 'imgur.com/a/' in proof:
                    embed.add_field(name=':camera_with_flash: Proof', value=proof, inline=False)
                    embed.set_image(url=json.loads(
                        get('https://api.imgur.com/3/album/' + proof.split('imgur.com/a/')[1] + '/images',
                            headers={'authorization': 'Client-ID ' + self.imgur_clientid}).text)["data"][0]['link'])
                else:
                    extensions = {".jpg", ".jpeg", ".png", ".gif"}
                    if any(proof.lower().endswith(ext) for ext in extensions):
                        embed.set_image(url=proof)
                        embed.add_field(name=':camera_with_flash: Proof', value=proof, inline=False)
                    else:
                        embed.add_field(name=':camera_with_flash: Proof', value=proof, inline=False)
                embed.colour = discord.Color.red()
        else:
            embed.add_field(name='Banned', value='Unknown âš ')
            embed.colour = discord.Color.orange()
        await self.bot.say(embed=embed)

    @commands.command()
    async def banlist(self, ctx, reload: bool = True):
        """Checks user for gloabal bans, use banlist true to refresh"""

        if reload: self.discordbans = \
            json.loads(post('https://bans.discordlist.net/listing', data=[('token', self.token)]).text)["data"]
        names = []
        for member in ctx.guild.members:
            if self.banned(member.id):
                names.append("``{}`` -- ``{}`` \n".format(str(member), str(member.id),))
        em = discord.Embed(
            description="**Found `{}` members out of `{}` Global Bans on DiscordList.net!**".format(len(names), len(
                self.discordbans)), colour=discord.Color.red())
        for member in ctx.guild.members:
            if self.banned(member.id):
                names.append("``{}`` -- ``{}`` \n".format(str(member), str(member.id),))
                em.add_field(name=member, value=member.id)
        embedperm = ctx.message.guild.me.permissions_in(ctx.message.channel).embed_links
        if embedperm is True:
            await self.bot.say(embed=em)
        else:
            await self.bot.say("**Found `{}` members out of `{}` Global Bans on DiscordList.net!**".format(len(names), len
            (self.discordbans)) + ("\n\nUsername -- ID\n" + "".join(names) + "" if len(names) > 0 else ""))
def setup(bot):
    bot.add_cog(DiscordBans(bot))
