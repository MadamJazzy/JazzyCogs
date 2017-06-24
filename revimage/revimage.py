from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup


class revimage:
    """Reverse image search commands"""
    def __init__(self, bot):
        self.bot = bot
        self.tineye_session = aiohttp.ClientSession()

    def __unload(self):
        self.tineye_session.close()

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
                await self.bot.delete_message(ctx.message)
            async with self.tineye_session.get('https://tineye.com/search/?url={}'.format(url)) as response:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                pages = []
                image_link = None
                try:
                    hidden = soup.find(class_='match').select('.hidden-xs')[0]
                    if hidden.contents[0].startswith('Page:'):
                        pages.append('<{}>'.format(hidden.next_sibling['href']))
                    else:
                        image_link = hidden.a['href']
                except AttributeError:
                    embed = discord.Embed(title="Reverse Image Details", color=0xffff00)
                    embed.add_field(name="Original Link", value="<{}>'.format(URL)", inline=False)
                    embed.add_field(name="Matches", value="**No Matches Found**", inline=False)
                    embed.add_field(name="Full Search", value="https://tineye.com/search/?url={}'.format(url)", inline=False)
#                    message = '\n**No matches found**\n'
#                    message += '\n**Full Search:**\nhttps://tineye.com/search/?url={}'.format(url)
#            message = '\n**Pages:** '
#            message += '\n**Pages:** '.join(pages)
            if image_link is not None:
                embed = discord.Embed(title="Reverse Image Details", color=0xffff00)
                embed.add_field(name="Original Link", value="<{}>'.format(URL)", inline=False)
                embed.add_field(name="Matches", value="<{}>'.format(image_link)", inline=False)
                embed.add_field(name="Full Search", value="https://tineye.com/search/?url={}'.format(url)", inline=False)
                await self.bot.say(embed=embed)
#                message = '\n**Image Found:** \n<{}>'.format(image_link)
#                message += '\n**Full Search:** \nhttps://tineye.com/search/?url={}'.format(url)
#            await self.bot.reply(message)
            await self.bot.reply(embed=embed)


def setup(bot):
    bot.add_cog(revimage(bot))
