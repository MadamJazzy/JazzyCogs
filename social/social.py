import discord
import random
import yaml
from pathlib import Path

from discord.ext import commands


def config():
    with open("cogs/social.yaml", 'r') as f:
        return yaml.safe_load(f)

class Social:

    def __init__(self, bot):
        self.bot = bot

    def embed_maker(self, ctx, action, user, sender,):
        with open ("data/social/social.yaml", 'r') as f:
            data = yaml.safe_load(f)
        if user == sender:
            msg = data[action]['selfmsg']
        else:
            msg = data[action]['msg']
        num = random.randint(1, int(data[action]['num']))
        if action == "fever":
            filetype = ".jpg"
        else:
            filetype = ".gif"
        baseurl = "http://cdn.hardinserver.com/social/"
        url = f'{baseurl}{action}/{action}{num}{filetype}'
        embed = discord.Embed(title=msg.format(sender.name, user.name))
        embed.set_image(url=url)
        return embed

    @commands.command(pass_context=True, invoke_without_command=True)
    async def kiss(self, ctx, *, user: discord.Member, action="kiss"):
        """Kiss people!"""
        await self.bot.say(embed=self.embed_maker(ctx, action, user, sender=ctx.message.author))


    @commands.command(pass_context=True, invoke_without_command=True)
    async def bite(self, ctx, *, user: discord.Member, action="bite"):
        """Bite people!"""
        await self.bot.say(embed=self.embed_maker(ctx, action, user, sender=ctx.message.author))

    @commands.command(pass_context=True, invoke_without_command=True)
    async def slap(self, ctx, *, user: discord.Member, action="slap"):
        """Slap people!"""
        await self.bot.say(embed=self.embed_maker(ctx, action, user, sender=ctx.message.author))

    @commands.command(pass_context=True, invoke_without_command=True)
    async def taunt(self, ctx, *, user: discord.Member, action="taunt"):
        """Taunt people!"""
        await self.bot.say(embed=self.embed_maker(ctx, action, user, sender=ctx.message.author))

    @commands.command(pass_context=True, invoke_without_command=True)
    async def cuddle(self, ctx, *, user: discord.Member, action="cuddle"):
        """Cuddle people!"""
        await self.bot.say(embed=self.embed_maker(ctx, action, user, sender=ctx.message.author))

    @commands.command(pass_context=True, invoke_without_command=True)
    async def hugs(self, ctx, *, user: discord.Member, action="hug"):
        """Hug people!"""
        await self.bot.say(embed=self.embed_maker(ctx, action, user, sender=ctx.message.author))

    @commands.command(pass_context=True, invoke_without_command=True)
    async def feed(self, ctx, *, user: discord.Member, action="feed"):
        """Feed people!"""
        await self.bot.say(embed=self.embed_maker(ctx, action, user, sender=ctx.message.author))

    @commands.command(pass_context=True, invoke_without_command=True)
    async def spank(self, ctx, *, user: discord.Member, action="spank"):
        """Spank people!"""
        await self.bot.say(embed=self.embed_maker(ctx, action, user, sender=ctx.message.author))

    @commands.command(pass_context=True, invoke_without_command=True)
    async def tease(self, ctx, *, user: discord.Member, action="tease"):
        """Tease people!"""
        await self.bot.say(embed=self.embed_maker(ctx, action, user, sender=ctx.message.author))

    @commands.command(pass_context=True, invoke_without_command=True)
    async def hi5(self, ctx, *, user: discord.Member, action="hi5"):
        """HighFive people!"""
        await self.bot.say(embed=self.embed_maker(ctx, action, user, sender=ctx.message.author))

    @commands.command(pass_context=True, invoke_without_command=True)
    async def shoot(self, ctx, *, user: discord.Member, action="shoot"):
        """Shoot people!"""
        await self.bot.say(embed=self.embed_maker(ctx, action, user, sender=ctx.message.author))

    @commands.command(pass_context=True, invoke_without_command=True)
    async def lick(self, ctx, *, user: discord.Member, action="lick"):
        """Lick people!"""
        await self.bot.say(embed=self.embed_maker(ctx, action, user, sender=ctx.message.author))

    @commands.command(pass_context=True, invoke_without_command=True)
    async def shake(self, ctx, *, user: discord.Member, action="shake"):
        """Handshake!"""
        await self.bot.say(embed=self.embed_maker(ctx, action, user, sender=ctx.message.author))

    @commands.command(pass_context=True, invoke_without_command=True)
    async def twerk(self, ctx, *, user: discord.Member, action="twerk"):
        """TWERK!"""
        await self.bot.say(embed=self.embed_maker(ctx, action, user, sender=ctx.message.author))

    @commands.command(pass_context=True, invoke_without_command=True)
    async def strip(self, ctx, *, user: discord.Member, action="strip"):
        """STRIP!"""
        await self.bot.say(embed=self.embed_maker(ctx, action, user, sender=ctx.message.author))

    @commands.command(pass_context=True, invoke_without_command=True)
    async def thirsty(self, ctx, *, user: discord.Member, action="thirsty"):
        """The Thirst is Real!"""
        await self.bot.say(embed=self.embed_maker(ctx, action, user, sender=ctx.message.author))

    @commands.command(pass_context=True, invoke_without_command=True)
    async def moist(self, ctx, *, user: discord.Member, action="moist"):
        """Moist lol!"""
        await self.bot.say(embed=self.embed_maker(ctx, action, user, sender=ctx.message.author))

    @commands.command(pass_context=True, invoke_without_command=True)
    async def whip(self, ctx, *, user: discord.Member, action="whip"):
        """Whip someone!"""
        await self.bot.say(embed=self.embed_maker(ctx, action, user, sender=ctx.message.author))

    @commands.command(pass_context=True, invoke_without_command=True)
    async def facepalm(self, ctx, *, user: discord.Member, action="facepalm"):
        """Facepalm images!"""
        await self.bot.say(embed=self.embed_maker(ctx, action, user, sender=ctx.message.author))

    @commands.command(pass_context=True, invoke_without_command=True)
    async def ohno(self, ctx, *, user: discord.Member, action="ono"):
        """Oh no they didnt images!"""
        await self.bot.say(embed=self.embed_maker(ctx, action, user, sender=ctx.message.author))

    @commands.command(pass_context=True, invoke_without_command=True)
    async def hungry(self, ctx, *, user: discord.Member, action="hungry"):
        """Hungry images!"""
        await self.bot.say(embed=self.embed_maker(ctx, action, user, sender=ctx.message.author))

    @commands.command(pass_context=True, invoke_without_command=True)
    async def nuts(self, ctx, *, user: discord.Member, action="nuts"):
        """NutCracker images!"""
        await self.bot.say(embed=self.embed_maker(ctx, action, user, sender=ctx.message.author))

    @commands.command(pass_context=True, invoke_without_command=True)
    async def fever(self, ctx, action="fever"):
        """Do you have the Fever?"""
        user = ctx.message.author
        await self.bot.say(embed=self.embed_maker(ctx, action, user, sender=ctx.message.author))

    @commands.command(pass_context=True, invoke_without_command=True)
    async def socialcmds(self):
        """List all Social Commands"""
        await self.bot.say("```Social Commands\n"
                           "kiss, bite, slap, taunt, cuddle, hugs, feed, spank, tease, hi5, shoot, lick, shake, shoot, "
                           "twerk, strip, thirsty, moist, whip, facepalm, ohno, hungry, nuts, fever, socialcmds ```")


def setup(bot):
    bot.add_cog(Social(bot))
