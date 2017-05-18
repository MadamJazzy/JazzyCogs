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

  async def upload_random_gif(self, msg, folder):
    if msg:
      await self.bot.say(msg)
    folderPath = "data/social/" + folder
    fileList = os.listdir(folderPath)
    gifPath = folderPath + "/" + fileList[randint(0, len(fileList) - 1)]
    await self.bot.upload(gifPath)

def setup(bot):
    bot.add_cog(Social(bot))

