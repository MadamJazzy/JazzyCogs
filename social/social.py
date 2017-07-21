import os
import asyncio
from random import randint, sample

import discord
from discord.ext import commands

class Social:
  def __init__(self, bot):
    self.bot = bot

sender=ctx.message.author.mention

  @commands.command(pass_context=True, invoke_without_command=True)
  async def kiss(self, ctx, *, user : discord.Member):
    """Kiss people!"""
    folder = "kiss"
    if ctx.message.author == user:
      await self.bot.say(sender + " You pervert! You cannot do that to yourself!")
    else:
      await self.upload_random_gif(user.mention + " was KISSED by " + sender + "! :kiss:", folder)


  @commands.command(pass_context=True, invoke_without_command=True)
  async def bite(self, ctx, *, user : discord.Member):
    """Bite people!"""
    folder = "bite"
    if ctx.message.author == user:
      await self.bot.say(sender + " As kinky as that is, I can't let you do that to yourself!")
    else:
      await self.upload_random_gif(user.mention + " was BITTEN by " + sender + "! ", folder)
      
  @commands.command(pass_context=True, invoke_without_command=True)
  async def slap(self, ctx, *, user : discord.Member):
    """Slap people!"""
    folder = "slap"
    if ctx.message.author == user:
      await self.bot.say(sender + " You Masochist! You cannot do that to yourself!")
    else:
      await self.upload_random_gif(user.mention + " was SLAPPED by " + sender.mention + " and i think they liked it! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def taunt(self, ctx, *, user : discord.Member):
    """Taunt people!"""
    folder = "taunt"
    if ctx.message.author == user:
      await self.bot.say(sender + " You must be really lonely? Do you need a friend? ")
    else:
      await self.upload_random_gif(user.mention + " was TAUNTED by " + sender + "! ", folder)
    
  @commands.command(pass_context=True, invoke_without_command=True)
  async def cuddle(self, ctx, *, user : discord.Member):
    """Cuddle people!"""
    folder = "cuddle"
    if ctx.message.author == user:
      await self.bot.say(sender + " I am sorry that you are so lonely, but you cannot Cuddle with yourself, Thats masterbation! ")
    else:
      await self.upload_random_gif(user.mention + " CUDDLES HARD with " + sender + " , and they like it! ", folder)


  @commands.command(pass_context=True, invoke_without_command=True)
  async def hugs(self, ctx, *, user : discord.Member):
    """Hug people!"""
    folder = "hug"
    if ctx.message.author == user:
      await self.bot.say(sender + "Aww... Do you need a friend?")
    else:
      await self.upload_random_gif(user.mention + " was given a BIG hug from " + sender + "! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def feed(self, ctx, *, user : discord.Member):
    """Feed people!"""
    folder = "feeds"
    if ctx.message.author == user:
      await self.bot.say(sender + " I'm so glad you know how to feed yourself! ")
    else:
      await self.upload_random_gif(user.mention + " was FED by " + sender + "! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def spank(self, ctx, *, user : discord.Member):
    """Spank people!"""
    folder = "spank"
    if ctx.message.author == user:
      await self.bot.say(sender + " I NEED AN ADULT!!! You cannot use me to spank yourself. Thats Nasty! ")
    else:
      await self.upload_random_gif(user.mention + " was SPANKED HARD by " + sender + " , and they LOVED it! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def tease(self, ctx, *, user : discord.Member):
    """Tease people!"""
    folder = "tease"
    if ctx.message.author == user:
      await self.bot.say(sender + " You're a special person aren't you? You cannot tease yourself! ")
    else:
      await self.upload_random_gif(user.mention + " was TEASED by " + sender + "! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def hi5(self, ctx, *, user : discord.Member):
    """HighFive people!"""
    folder = "hi5"
    if ctx.message.author == user:
      await self.bot.say(sender + " Nice try, You have to get out more! ")
    else:
      await self.upload_random_gif(user.mention + " was HIGHFIVED by " + sender + "! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def shoot(self, ctx, *, user : discord.Member):
    """Shoot people!"""
    folder = "shoot"
    if ctx.message.author == user:
      await self.bot.say(sender + " Calm down! I am sure we can solve whatever problem you're having. ")
    else:
      await self.upload_random_gif(user.mention + " was SHOT by " + sender + "! They survived! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def lick(self, ctx, *, user : discord.Member):
    """Lick people!"""
    folder = "lick"
    if ctx.message.author == user:
      await self.bot.say(sender + " Well aren't you a kinky little thing? And very flexible! ")
    else:
      await self.upload_random_gif(user.mention + " was LICKED by " + sender + "! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def shake(self, ctx, *, user : discord.Member):
    """Handshake!"""
    folder = "handshake"
    if ctx.message.author == user:
      await self.bot.say(sender + " No, Just No! Get a life! ")
    else:
      await self.upload_random_gif(user.mention + " Shook " + sender + "'s Hand! ", folder)
      
  @commands.command(pass_context=True, invoke_without_command=True)
  async def twerk(self, ctx, *, user : discord.Member):
    """TWERK!"""
    folder = "twerk"
    if ctx.message.author == user:
      await self.bot.say(sender + " Did you just try to twerk on yourself? We'll pretend that never happened! ")
    else:
      await self.upload_random_gif(user.mention + " TWERKED FOR " + sender + "! and they LIKED it! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def strip(self, ctx, *, user : discord.Member):
    """STRIP!"""
    folder = "strip"
    if ctx.message.author == user:
      await self.bot.say(sender + " No, Just No! Get a life! ")
    else:
      await self.upload_random_gif(sender + " strips for " + user.mention + " and they LIKE it! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def thirsty(self, ctx, *, user : discord.Member):
    """The Thirst is Real!"""
    folder = "thirsty"
    if ctx.message.author == user:
      await self.bot.say(sender.mention + " Really? Just really?? You need help! ")
    else:
      await self.upload_random_gif(sender + " tells " + user.mention + " To calm your thirsty ass down! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def moist(self, ctx, *, user : discord.Member):
    """Moist lol!"""
    folder = "moist"
    if ctx.message.author == user:
      await self.bot.say(sender.mention + " You are way to easy! ")
    else:
      await self.upload_random_gif(user.mention + " has made " + sender + " moist. OH LORD! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def whip(self, ctx, *, user : discord.Member):
    """Whip someone!"""
    folder = "whip"
    if ctx.message.author == user:
      await self.bot.say(sender + " Well aren't you just a kinky thing! ")
    else:
      await self.upload_random_gif(sender + " has whipped " + user.mention + " and i think they LIKED it! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def facepalm(self, ctx, *, user : discord.Member):
    """Facepalm images!"""
    folder = "facepalm"
    if ctx.message.author == user:
      await self.bot.say(sender.mention + " You cannot do that to yourself! ")
    else:
      await self.upload_random_gif(user.mention + " has made " + sender + " FACEPALM! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def ohno(self, ctx, *, user : discord.Member):
    """Oh no they didnt images!"""
    folder = "ono"
    if ctx.message.author == user:
      await self.bot.say(sender + " Oh No you didn't? Well then don't do it again. ")
    else:
      await self.upload_random_gif(sender + " yells at " + user.mention + " Oh no they didn't! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def hungry(self, ctx, *, user : discord.Member):
    """Hungry images!"""
    folder = "hungry"
    if ctx.message.author == user:
      await self.bot.say(sender.mention + " THEN GO GET SOMETHING TO EAT! ")
    else:
      await self.upload_random_gif(user.mention + " has made " + sender + " HUNGRY! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def nuts(self, ctx, *, user : discord.Member):
    """NutCracker images!"""
    folder = "nuts"
    if ctx.message.author == user:
      await self.bot.say(sender.mention + " KINKY! You can sit by me!! ")
    else:
      await self.upload_random_gif(sender + " wants to hit " + user.mention + " in the NUTS! OUCH!! ", folder)

  async def upload_random_gif(self, msg, folder):
    if msg:
      await self.bot.say(msg)
    folderPath = "data/social/" + folder
    fileList = os.listdir(folderPath)
    gifPath = folderPath + "/" + fileList[randint(0, len(fileList) - 1)]
    await self.bot.upload(gifPath)

def setup(bot):
    bot.add_cog(Social(bot))

