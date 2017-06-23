from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup

#WIP-This cog will not work correctly as is. 
class revimage:
    """Reverse image search commands"""
    def __init__(self, bot):
        self.bot = bot
        self.sauce_session = aiohttp.ClientSession()
        self.tineye_session = aiohttp.ClientSession()
        self.google_session = aiohttp.ClientSession()

    def __unload(self):
        self.sauce_session.close()
        self.tineye_session.close()
        self.google_session.close()

    def _tag_to_title(self, tag):
        return tag.replace(' ', ', ').replace('_', ' ').title()

    @commands.command(pass_context=True)
    async def tineye(self, ctx, link=None):
        """
        Reverse image search using tineye
        usage:  .tineye <image-link> or
                .tineye on image upload comment
        """
        file = ctx.message.attachments
        if link is None and not file:
            await self.bot.say('Message didn\'t contain Image')
        else:
            await self.bot.type()
            if file:
                url = file[0]['proxy_url']
            else:
                url = link
            async with self.tineye_session.get('https://tineye.com/search/?url={}'.format(url)) as response:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                pages = []
                image_link = None
                hidden = soup.find(class_='match').select('.hidden-xs')[0]
                if hidden.contents[0].startswith('Page:'):
                    pages.append('<{}>'.format(hidden.next_sibling['href']))
                else:
                    image_link = hidden.a['href']
#            message = '\n**Pages:** '
#            message += '\n**Pages:** '.join(pages)
            if image_link is not None:
                message = '\n**Image Found:** \n<{}>'.format(image_link)
            else:
                message = '\n**Image not Found'
            await self.bot.embed(message)

    @commands.command(pass_context=True)
    async def gimage(self, ctx, link=None):
        """
        Reverse image search using google
        usage:  .gimage <image-link> or
                .gimage on image upload comment
        """
        file = ctx.message.attachments
        if link is None and not file:
            await self.bot.say('Message didn\'t contain Image')
        else:
            await self.bot.type()
            if file:
                url = file[0]['proxy_url']
            else:
                url = link
            async with self.google_session.get('https://www.google.com/searchbyimage?image_url={}'.format(url)) as response:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                pages = []
                image_link = None
                hidden = soup.find(class_='match').select('.hidden-xs')[0]
                if hidden.contents[0].startswith('Page:'):
                    pages.append('<{}>'.format(hidden.next_sibling['href']))
                else:
                    image_link = hidden.a['href']
            message = '\n**Pages:** '
            message += '\n**Pages:** '.join(pages)
            if image_link is not None:
                message += '\n**direct image:** <{}>'.format(image_link)
            await self.bot.reply(message)


def setup(bot):
    bot.add_cog(revimage(bot))
