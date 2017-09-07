import discord, asyncio
from requests import post, get
from discord.ext import commands
from cogs.utils.checks import *

class DiscordBans:
    """Utilizes DiscordList.com's Banlist"""
    version = 1
    url = "https://raw.githubusercontent.com/Bluscream/ASCII/master/cogs/discordbans.json"
    class author(discord.ClientUser):
        name = "Bluscream"
        discriminator = "2597"
        id = 97138137679028224
        email = "bluscreamlp@gmail.com"
    # Cog Variables
    token = 'rnRKaAhkVX'
    imgur_clientid = 'aa3bde928fe4e09'

    def __init__(self, bot):
        self.bot = bot
        self.discordbans = json.loads(post('https://bans.discordlist.net/listing', data=[('token', self.token)]).text)["data"]

    def banned(self, uid):
        if len(self.discordbans) > 0:
            for ban in self.discordbans:
                if uid == int(ban[1]):
                    return ban
            return False

    @commands.command(aliases=["dbl"], pass_context=True)
    async def discordbanlist(self, ctx, *, uid: int=None, reload: bool=False):
        await ctx.message.delete()
        if not uid: uid = self.bot.user.id
        if reload: self.discordbans = json.loads(post('https://bans.discordlist.net/listing', data=[('token', self.token)]).text)["data"]
        embed = discord.Embed(description='\🔨 **Ban Lookup for** <@{}>'.format(uid),colour=discord.Color.green())
        _gban = self.banned(uid)
        if _gban is not None:
            if not _gban: embed.description = embed.description + '\n\nNot banned \✅'
            else:
                # embed.add_field(name=':hammer: Banned', value='Yes \❌')
                embed.add_field(name=':pencil2: Name', value='`{}`'.format(_gban[0]))
                embed.add_field(name=':card_index: ID', value=_gban[1])
                embed.add_field(name=':notepad_spiral: Reason', value='``` {} ```'.format(_gban[2]))
                proof = _gban[3].replace('<a href="','').replace('">Proof</a>','')
                if 'imgur.com/a/' in proof:
                    embed.add_field(name=':camera_with_flash: Proof', value=proof, inline=False)
                    embed.set_image(url=json.loads(get('https://api.imgur.com/3/album/'+proof.split('imgur.com/a/')[1]+'/images',headers={'authorization': 'Client-ID '+self.imgur_clientid}).text)["data"][0]['link'])
                else:
                    extensions = {".jpg", ".jpeg", ".png", ".gif"}
                    if any(proof.lower().endswith(ext) for ext in extensions):
                        embed.set_image(url=proof)
                    else:
                        embed.add_field(name=':camera_with_flash: Proof', value=proof, inline=False)
                embed.colour=discord.Color.red()
        else:
            embed.add_field(name='Banned', value='Unknown ⚠')
            embed.colour=discord.Color.orange()
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(DiscordBans(bot))