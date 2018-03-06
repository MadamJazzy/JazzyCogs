import os
import asyncio
from random import randint, sample

import discord
from discord.ext import commands


class Social:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, invoke_without_command=True)
    async def kiss(self, ctx, *, user: discord.Member):
        """Kiss people!"""
        sender = ctx.message.author
        folder = "kiss"
        if ctx.message.author == user:
            await self.bot.say("``" + sender.name + "``"  + " You pervert! You cannot do that to yourself!")
        else:
            await self.upload_random_gif("``" + user.name + "``" + " was KISSED by " + "``" + sender.name + "``" + "! :kiss:", folder)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def bite(self, ctx, *, user: discord.Member):
        """Bite people!"""
        sender = ctx.message.author
        folder = "bite"
        if ctx.message.author == user:
            await self.bot.say("``" + sender.name + "``"  + " As kinky as that is, I can't let you do that to yourself!")
        else:
            await self.upload_random_gif("``" + user.name + "``"  + " was BITTEN by " + "``" + sender.name + "``"  + "! ", folder)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def slap(self, ctx, *, user: discord.Member):
        """Slap people!"""
        sender = ctx.message.author
        folder = "slap"
        if ctx.message.author == user:
            await self.bot.say("``" + sender.name + "``"  + " You Masochist! You cannot do that to yourself!")
        else:
            await self.upload_random_gif(
                "``" + user.name + "``"  + " was SLAPPED by " + "``" + sender.name + "``"  + " and i think they liked it! ", folder)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def taunt(self, ctx, *, user: discord.Member):
        """Taunt people!"""
        sender = ctx.message.author
        folder = "taunt"
        if ctx.message.author == user:
            await self.bot.say("``" + sender.name + "``"  + " You must be really lonely? Do you need a friend? ")
        else:
            await self.upload_random_gif("``" + user.name + "``"  + " was TAUNTED by " + "``" + sender.name + "``"  + "! ", folder)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def cuddle(self, ctx, *, user: discord.Member):
        """Cuddle people!"""
        sender = ctx.message.author
        folder = "cuddle"
        if ctx.message.author == user:
            await self.bot.say(
                "``" + sender.name + "``"  + " I am sorry that you are so lonely, but you cannot Cuddle with yourself, Thats masterbation! ")
        else:
            await self.upload_random_gif(
                "``" + user.name + "``"  + " CUDDLES HARD with " + "``" + sender.name + "``"  + " , and they like it! ", folder)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def hugs(self, ctx, *, user: discord.Member):
        """Hug people!"""
        sender = ctx.message.author
        folder = "hug"
        if ctx.message.author == user:
            await self.bot.say("``" + sender.name + "``"  + " Sorry, you are not that flexible. You cannot Hug yourself!")
        else:
            await self.upload_random_gif("``" + user.name + "``"  + " was given a BIG hug from " + "``" + sender.name + "``"  + "! ", folder)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def feed(self, ctx, *, user: discord.Member):
        """Feed people!"""
        sender = ctx.message.author
        folder = "feeds"
        if ctx.message.author == user:
            await self.bot.say("``" + sender.name + "``"  + " I'm so glad you know how to feed yourself! ")
        else:
            await self.upload_random_gif("``" + user.name + "``"  + " was FED by " + "``" + sender.name + "``"  + "! ", folder)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def spank(self, ctx, *, user: discord.Member):
        """Spank people!"""
        sender = ctx.message.author
        folder = "spank"
        if ctx.message.author == user:
            await self.bot.say(
                "``" + sender.name + "``"  + " I NEED AN ADULT!!! You cannot use me to spank yourself. Thats Nasty! ")
        else:
            await self.upload_random_gif(
                "``" + user.name + "``"  + " was SPANKED HARD by " + "``" + sender.name + "``"  + " , and they LOVED it! ", folder)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def tease(self, ctx, *, user: discord.Member):
        """Tease people!"""
        sender = ctx.message.author
        folder = "tease"
        if ctx.message.author == user:
            await self.bot.say("``" + sender.name + "``"  + " You're a special person aren't you? You cannot tease yourself! ")
        else:
            await self.upload_random_gif("``" + user.name + "``"  + " was TEASED by " + "``" + sender.name + "``"  + "! ", folder)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def hi5(self, ctx, *, user: discord.Member):
        """HighFive people!"""
        sender = ctx.message.author
        folder = "hi5"
        if ctx.message.author == user:
            await self.bot.say("``" + sender.name + "``"  + " Nice try, You have to get out more! ")
        else:
            await self.upload_random_gif("``" + user.name + "``"  + " was HIGHFIVED by " + "``" + sender.name + "``"  + "! ", folder)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def shoot(self, ctx, *, user: discord.Member):
        """Shoot people!"""
        sender = ctx.message.author
        folder = "shoot"
        if ctx.message.author == user:
            await self.bot.say("``" + sender.name + "``"  + " Calm down! I am sure we can solve whatever problem you're having. ")
        else:
            await self.upload_random_gif("``" + user.name + "``"  + " was SHOT by " + "``" + sender.name + "``"  + "! They survived! ", folder)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def lick(self, ctx, *, user: discord.Member):
        """Lick people!"""
        sender = ctx.message.author
        folder = "lick"
        if ctx.message.author == user:
            await self.bot.say("``" + sender.name + "``"  + " Well aren't you a kinky little thing? And very flexible! ")
        else:
            await self.upload_random_gif("``" + user.name + "``"  + " was LICKED by " + "``" + sender.name + "``"  + "! ", folder)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def shake(self, ctx, *, user: discord.Member):
        """Handshake!"""
        sender = ctx.message.author
        folder = "handshake"
        if ctx.message.author == user:
            await self.bot.say("``" + sender.name + "``"  + " No, Just No! Get a life! ")
        else:
            await self.upload_random_gif("``" + user.name + "``"  + " Shook " + "``" + sender.name + "``"  + "'s Hand! ", folder)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def twerk(self, ctx, *, user: discord.Member):
        """TWERK!"""
        sender = ctx.message.author
        folder = "twerk"
        if ctx.message.author == user:
            await self.bot.say(
                "``" + sender.name + "``"  + " Did you just try to twerk on yourself? We'll pretend that never happened! ")
        else:
            await self.upload_random_gif("``" + user.name + "``"  + " TWERKED FOR " + "``" + sender.name + "``"  + "! and they LIKED it! ",
                                         folder)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def strip(self, ctx, *, user: discord.Member):
        """STRIP!"""
        sender = ctx.message.author
        folder = "strip"
        if ctx.message.author == user:
            await self.bot.say("``" + sender.name + "``"  + " No, Just No! Get a life! ")
        else:
            await self.upload_random_gif("``" + sender.name + "``"  + " strips for " + "``" + user.name + "``"  + " and they LIKE it! ", folder)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def thirsty(self, ctx, *, user: discord.Member):
        """The Thirst is Real!"""
        sender = ctx.message.author
        folder = "thirsty"
        if ctx.message.author == user:
            await self.bot.say("``" + sender.name + "``"  + " Really? Just really?? You need help! ")
        else:
            await self.upload_random_gif("``" + sender.name + "``"  + " tells " + "``" + user.name + "``"  + " To calm your thirsty ass down! ",
                                         folder)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def moist(self, ctx, *, user: discord.Member):
        """Moist lol!"""
        sender = ctx.message.author
        folder = "moist"
        if ctx.message.author == user:
            await self.bot.say("``" + sender.name + "``"  + " You are way to easy! ")
        else:
            await self.upload_random_gif("``" + user.name + "``"  + " has made " + "``" + sender.name + "``"  + " moist. OH LORD! ", folder)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def whip(self, ctx, *, user: discord.Member):
        """Whip someone!"""
        sender = ctx.message.author
        folder = "whip"
        if ctx.message.author == user:
            await self.bot.say("``" + sender.name + "``"  + " Well aren't you just a kinky thing! ")
        else:
            await self.upload_random_gif(
                "``" + sender.name + "``"  + " has whipped " + "``" + user.name + "``"  + " and i think they LIKED it! ", folder)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def facepalm(self, ctx, *, user: discord.Member):
        """Facepalm images!"""
        sender = ctx.message.author
        folder = "facepalm"
        if ctx.message.author == user:
            await self.bot.say("``" + sender.name + "``"  + " You cannot do that to yourself! ")
        else:
            await self.upload_random_gif("``" + user.name + "``"  + " has made " + "``" + sender.name + "``"  + " FACEPALM! ", folder)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def ohno(self, ctx, *, user: discord.Member):
        """Oh no they didnt images!"""
        sender = ctx.message.author
        folder = "ono"
        if ctx.message.author == user:
            await self.bot.say("``" + sender.name + "``"  + " You cannot do that to yourself! ")
        else:
            await self.upload_random_gif("``" + sender.name + "``"  + " yells at " + "``" + user.name + "``"  + " Oh no they didn't! ", folder)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def hungry(self, ctx, *, user: discord.Member):
        """Hungry images!"""
        sender = ctx.message.author
        folder = "hungry"
        if ctx.message.author == user:
            await self.bot.say("``" + sender.name + "``"  + " THEN GO GET SOMETHING TO EAT! ")
        else:
            await self.upload_random_gif("``" + user.name + "``"  + " has made " + "``" + sender.name + "``"  + " HUNGRY! ", folder)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def nuts(self, ctx, *, user: discord.Member):
        """NutCracker images!"""
        sender = ctx.message.author
        folder = "nuts"
        if ctx.message.author == user:
            await self.bot.say("``" + sender.name + "``"  + " No, Just no! Get a life! ")
        else:
            await self.upload_random_gif("``" + sender.name + "``"  + " wants to kick " + "``" + user.name + "``"  + " in the NUTS! OUCH!! ",
                                         folder)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def fever(self, ctx):
        """Do you have the Fever?"""
        sender = ctx.message.author
        folder = "fever"
        await self.upload_random_gif("``" + sender.name + "``"  + "I see you have the fever.... The Bieber fever", folder)


    async def upload_random_gif(self, msg, folder):
        if msg:
            await self.bot.say(msg)
        folderPath = "data/social/" + folder
        fileList = os.listdir(folderPath)
        gifPath = folderPath + "/" + fileList[randint(0, len(fileList) - 1)]
        await self.bot.upload(gifPath)


def setup(bot):
    bot.add_cog(Social(bot))
