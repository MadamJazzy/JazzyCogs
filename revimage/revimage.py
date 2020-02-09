from discord.ext import commands
import discord


class revimage:
    """Reverse image search commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def revimg(self, ctx, url=None):
        """Reverse Image Search using several popular reverse search services.
        usage:  [p]revimg <image-link> or
        [p]revimg on image upload comment"""
        if url is not None:
            await ctx.message.delete()
        if url is None:
            try:
                url = ctx.message.attachments[0].url
            except IndexError:
                return await ctx.send('No URL or Image detected. Please try again!')
        embed = discord.Embed(title='Reverse Image Details', color=16776960)
        embed.add_field(name="Sauce", value=f'[Sauce Image Results](https://saucenao.com/search.php?url={url})', inline=True)
        embed.add_field(name="Google", value=f'[Google Image Results](https://www.google.com/searchbyimage?&image_url={url})', inline=True)
        embed.add_field(name="TinEye", value=f'[Tineye Image Results](https://www.tineye.com/search?url={url})', inline=True)
        embed.add_field(name="IQBD", value=f'[IQBD Image Results](https://iqdb.org/?url={url})', inline=True)
        embed.add_field(name="Yandex", value=f'[Yandex Image Results](https://yandex.com/images/search?url={url}&rpt=imageview)', inline=True)
        embed.set_thumbnail(url=url)
        await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(revimage(bot))
