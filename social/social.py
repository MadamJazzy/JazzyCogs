import os
import asyncio
from random import randint, sample

import discord
from discord.ext import commands

class Social:
  def __init__(self, bot):
    self.bot = bot
  

  @commands.command(pass_context=True, invoke_without_command=True)
  async def kiss(self, ctx, *, user : discord.Member):
    """Kiss people!"""
    sender = ctx.message.author
    folder = "kiss"
    if ctx.message.author == user:
      await self.bot.say(sender.mention + " You pervert! You cannot do that to yourself!")
    else:
      await self.upload_random_gif(user.mention + " was KISSED by " + sender.mention + "! :kiss:", folder)


  @commands.command(pass_context=True, invoke_without_command=True)
  async def bite(self, ctx, *, user : discord.Member):
    """Bite people!"""
    sender = ctx.message.author
    folder = "bite"
    if ctx.message.author == user:
      await self.bot.say(sender.mention + " As kinky as that is, I can't let you do that to yourself!")
    else:
      await self.upload_random_gif(user.mention + " was BITTEN by " + sender.mention + "! ", folder)
      
  @commands.command(pass_context=True, invoke_without_command=True)
  async def slap(self, ctx, *, user : discord.Member):
    """Slap people!"""
    sender = ctx.message.author
    folder = "slap"
    if ctx.message.author == user:
      await self.bot.say(sender.mention + " You Masochist! You cannot do that to yourself!")
    else:
      await self.upload_random_gif(user.mention + " was SLAPPED by " + sender.mention + " and i think they liked it! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def gaykiss(self, ctx, *, user : discord.Member):
    """Kiss people(2 Men Gif)!"""
    sender = ctx.message.author
    folder = "gaykiss"
    if ctx.message.author == user:
      await self.bot.say(sender.mention + " You PERVERT! You cannot do that to yourself!")
    else:
      await self.upload_random_gif(user.mention + " was KISSED by " + sender.mention + "! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def taunt(self, ctx, *, user : discord.Member):
    """Taunt people!"""
    sender = ctx.message.author
    folder = "taunt"
    if ctx.message.author == user:
      await self.bot.say(sender.mention + " You must be really lonely? Do you need a friend? ")
    else:
      await self.upload_random_gif(user.mention + " was TAUNTED by " + sender.mention + "! ", folder)
    
  @commands.command(pass_context=True, invoke_without_command=True)
  async def cuddle(self, ctx, *, user : discord.Member):
    """Cuddle people!"""
    sender = ctx.message.author
    folder = "cuddle"
    if ctx.message.author == user:
      await self.bot.say(sender.mention + " I am sorry that you are so lonely, but you cannot Cuddle with yourself, Thats masterbation! ")
    else:
      await self.upload_random_gif(user.mention + " CUDDLES HARD with " + sender.mention + " , and they like it! ", folder)


  @commands.command(pass_context=True, invoke_without_command=True)
  async def hugs(self, ctx, *, user : discord.Member):
    """Hug people!"""
    sender = ctx.message.author
    folder = "hug"
    if ctx.message.author == user:
      await self.bot.say(sender.mention + " Sorry, you are not that flexible. You cannot Hug yourself!")
    else:
      await self.upload_random_gif(user.mention + " was given a BIG hug from " + sender.mention + "! ", folder) 
  

  @commands.command(pass_context=True, invoke_without_command=True)
  async def truth(self, ctx, *, user : discord.Member):
    """Truth Questions!"""
    sender = ctx.message.author
    folder = "truth"
    if ctx.message.author == user:
      await self.bot.say(sender.mention + " Nice try! You cannot do that with yourself!")
    else:
      await self.upload_random_gif(user.mention + " was asked a question by " + sender.mention + " who wants them to tell the TRUTH! ", folder) 

  @commands.command(pass_context=True, invoke_without_command=True)
  async def dare(self, ctx, *, user : discord.Member):
    """Dare Questions!"""
    sender = ctx.message.author
    folder = "dare"
    if ctx.message.author == user:
      await self.bot.say(sender.mention + " You CHEATER! You cannot Dare yourself to do something! ")
    else:
      await self.upload_random_gif(user.mention + " is challened to a DARE by " + sender.mention + "! ", folder)  
 
  @commands.command(pass_context=True, invoke_without_command=True)
  async def feed(self, ctx, *, user : discord.Member):
    """Feed people!"""
    sender = ctx.message.author
    folder = "feed"
    if ctx.message.author == user:
      await self.bot.say(sender.mention + " I'm so glad you know how to feed yourself! ")
    else:
      await self.upload_random_gif(user.mention + " was FED by " + sender.mention + "! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def spank(self, ctx, *, user : discord.Member):
    """Spank people!"""
    sender = ctx.message.author
    folder = "spank"
    if ctx.message.author == user:
      await self.bot.say(sender.mention + " I NEED AN ADULT!!! You cannot use me to spank yourself. Thats Nasty! ")
    else:
      await self.upload_random_gif(user.mention + " was SPANKED HARD by " + sender.mention + " , and they LOVED it! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def tease(self, ctx, *, user : discord.Member):
    """Tease people!"""
    sender = ctx.message.author
    folder = "tease"
    if ctx.message.author == user:
      await self.bot.say(sender.mention + " You're a special person aren't you? You cannot tease yourself! ")
    else:
      await self.upload_random_gif(user.mention + " was TEASED by " + sender.mention + "! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def hi5(self, ctx, *, user : discord.Member):
    """HighFive people!"""
    sender = ctx.message.author
    folder = "hi5"
    if ctx.message.author == user:
      await self.bot.say(sender.mention + " Nice try, You have to get out more! ")
      await self.bot.upload(data/social/self/1.gif)
    else:
      await self.upload_random_gif(user.mention + " was HIGHFIVED by " + sender.mention + "! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def shoot(self, ctx, *, user : discord.Member):
    """Shoot people!"""
    sender = ctx.message.author
    folder = "shoot"
    if ctx.message.author == user:
      await self.bot.say(sender.mention + " Calm down! I am sure we can solve whatever problem you're having. ")
    else:
      await self.upload_random_gif(user.mention + " was SHOT by " + sender.mention + "! They survived! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def lick(self, ctx, *, user : discord.Member):
    """Lick people!"""
    sender = ctx.message.author
    folder = "lick"
    if ctx.message.author == user:
      await self.bot.say(sender.mention + " Well aren't you a kinky little thing? And very flexible! ")
    else:
      await self.upload_random_gif(user.mention + " was LICKED by " + sender.mention + "! ", folder)

  @commands.command(pass_context=True, invoke_without_command=True)
  async def shake(self, ctx, *, user : discord.Member):
    """Handshake!"""
    sender = ctx.message.author
    folder = "handshake"
    if ctx.message.author == user:
      await self.bot.say(sender.mention + " No, Just No! Get a life! ")
    else:
      await self.upload_random_gif(user.mention + " Shook " + sender.mention + "'s Hand! ", folder)
      
  @commands.command(pass_context=True, invoke_without_command=True)
  async def twerk(self, ctx, *, user : discord.Member):
    """TWERK!"""
    sender = ctx.message.author
    folder = "twerk"
    if ctx.message.author == user:
      await self.bot.say(sender.mention + " Did you just try to twerk on yourself? We'll pretend that never happened! ")
    else:
      await self.upload_random_gif(user.mention + " TWERKED FOR " + sender.mention + "! and thet LIKED it! ", folder)

  async def upload_random_gif(self, msg, folder):
    if msg:
      await self.bot.say(msg)
    folderPath = "data/social/" + folder
    fileList = os.listdir(folderPath)
    gifPath = folderPath + "/" + fileList[randint(0, len(fileList) - 1)]
    await self.bot.upload(gifPath)

def setup(bot):
    bot.add_cog(Social(bot))

