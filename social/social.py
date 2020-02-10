import discord
import random
import yaml

from discord.ext import commands


class Social:

    def __init__(self, bot):
        self.bot = bot

    def config(self, action):
        with open("data.yml", "r") as data:
            return yaml.safe_load(data)[action]

    def embed_maker(self, action, user: discord.Member, sender: discord.Member, data):
        msg = self.testy(data, user, sender)
        num = random.randint(1, int(data['num']))
        if action == "fever":
            filetype = ".jpg"
        else:
            filetype = ".gif"
        url = f'{action}/{action}+({num}){filetype}'
        embed = discord.Embed(title=msg.format(sender.mention, user.mention))
        embed.set_image(url=url)
        return embed

    def testy(self, data, user, sender):
        if user == sender:
            return data['selfmsg']
        else:
            return data['msg']

    @commands.command(pass_context=True, invoke_without_command=True)
    async def kiss(self, ctx, *, user: discord.Member, action="kiss"):
        """Kiss people!"""
        self.embed_maker(action, user, sender=ctx.message.author, data=self.config(action))
        await self.bot.send_message(embed=embed)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def bite(self, ctx, *, user: discord.Member, action="bite"):
        """Bite people!"""
        self.embed_maker(action, user, sender=ctx.message.author, data=self.config(action))
        await self.bot.send_message(embed=embed)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def slap(self, ctx, *, user: discord.Member, action="slap"):
        """Slap people!"""
        self.embed_maker(action, user, sender=ctx.message.author, data=self.config(action))
        await self.bot.send_message(embed=embed)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def taunt(self, ctx, *, user: discord.Member, action="taunt"):
        """Taunt people!"""
        self.embed_maker(action, user, sender=ctx.message.author, data=self.config(action))
        await self.bot.send_message(embed=embed)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def cuddle(self, ctx, *, user: discord.Member, action="cuddle"):
        """Cuddle people!"""
        self.embed_maker(action, user, sender=ctx.message.author, data=self.config(action))
        await self.bot.send_message(embed=embed)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def hugs(self, ctx, *, user: discord.Member, action="hug"):
        """Hug people!"""
        self.embed_maker(action, user, sender=ctx.message.author, data=self.config(action))
        await self.bot.send_message(embed=embed)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def feed(self, ctx, *, user: discord.Member, action="feed"):
        """Feed people!"""
        self.embed_maker(action, user, sender=ctx.message.author, data=self.config(action))
        await self.bot.send_message(embed=embed)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def spank(self, ctx, *, user: discord.Member, action="spank"):
        """Spank people!"""
        self.embed_maker(action, user, sender=ctx.message.author, data=self.config(action))
        await self.bot.send_message(embed=embed)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def tease(self, ctx, *, user: discord.Member, action="tease"):
        """Tease people!"""
        self.embed_maker(action, user, sender=ctx.message.author, data=self.config(action))
        await self.bot.send_message(embed=embed)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def hi5(self, ctx, *, user: discord.Member, action="hi5"):
        """HighFive people!"""
        self.embed_maker(action, user, sender=ctx.message.author, data=self.config(action))
        await self.bot.send_message(embed=embed)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def shoot(self, ctx, *, user: discord.Member, action="shoot"):
        """Shoot people!"""
        self.embed_maker(action, user, sender=ctx.message.author, data=self.config(action))
        await self.bot.send_message(embed=embed)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def lick(self, ctx, *, user: discord.Member, action="lick"):
        """Lick people!"""
        self.embed_maker(action, user, sender=ctx.message.author, data=self.config(action))
        await self.bot.send_message(embed=embed)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def shake(self, ctx, *, user: discord.Member, action="shake"):
        """Handshake!"""
        self.embed_maker(action, user, sender=ctx.message.author, data=self.config(action))
        await self.bot.send_message(embed=embed)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def twerk(self, ctx, *, user: discord.Member, action="twerk"):
        """TWERK!"""
        self.embed_maker(action, user, sender=ctx.message.author, data=self.config(action))
        await self.bot.send_message(embed=embed)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def strip(self, ctx, *, user: discord.Member, action="strip"):
        """STRIP!"""
        self.embed_maker(action, user, sender=ctx.message.author, data=self.config(action))
        await self.bot.send_message(embed=embed)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def thirsty(self, ctx, *, user: discord.Member, action="thirsty"):
        """The Thirst is Real!"""
        self.embed_maker(action, user, sender=ctx.message.author, data=self.config(action))
        await self.bot.send_message(embed=embed)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def moist(self, ctx, *, user: discord.Member, action="moist"):
        """Moist lol!"""
        self.embed_maker(action, user, sender=ctx.message.author, data=self.config(action))
        await self.bot.send_message(embed=embed)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def whip(self, ctx, *, user: discord.Member, action="whip"):
        """Whip someone!"""
        self.embed_maker(action, user, sender=ctx.message.author, data=self.config(action))
        await self.bot.send_message(embed=embed)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def facepalm(self, ctx, *, user: discord.Member, action="facepalm"):
        """Facepalm images!"""
        self.embed_maker(action, user, sender=ctx.message.author, data=self.config(action))
        await self.bot.send_message(embed=embed)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def ohno(self, ctx, *, user: discord.Member, action="ono"):
        """Oh no they didnt images!"""
        self.embed_maker(action, user, sender=ctx.message.author, data=self.config(action))
        await self.bot.send_message(embed=embed)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def hungry(self, ctx, *, user: discord.Member, action="hungry"):
        """Hungry images!"""
        self.embed_maker(action, user, sender=ctx.message.author, data=self.config(action))
        await self.bot.send_message(embed=embed)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def nuts(self, ctx, *, user: discord.Member, action="nuts"):
        """NutCracker images!"""
        self.embed_maker(action, user, sender=ctx.message.author, data=self.config(action))
        await self.bot.send_message(embed=embed)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def fever(self, ctx, action="fever"):
        """Do you have the Fever?"""
        user = ctx.message.author
        self.embed_maker(action, user, sender=ctx.message.author, data=self.config(action))
        await self.bot.send_message(embed=embed)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def socialcmds(self):
        """List all Social Commands"""
        await self.bot.say("```Social Commands\n"
                           "kiss, bite, slap, taunt, cuddle, hugs, feed, spank, tease, hi5, shoot, lick, shake, shoot, "
                           "twerk, strip, thirsty, moist, whip, facepalm, ohno, hungry, nuts, fever, socialcmds ```")


def setup(bot):
    bot.add_cog(Social(bot))
