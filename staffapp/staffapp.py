import os
import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from cogs.utils import checks


class staffapp:
    """Custom Cog for applications"""
    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json('data/staffapp/settings.json')
        for s in self.settings:
            self.settings[s]['usercache'] = []
    def save_json(self):
        dataIO.save_json("data/staffapp/settings.json", self.settings)

    @commands.group(name="staffset", pass_context=True, no_pm=True)
    async def appset(self, ctx):
        """configuration settings"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
    def initial_config(self, server_id):
        """makes an entry for the server, defaults to turned off"""
        if server_id not in self.settings:
            self.settings[server_id] = {'inactive': True,
                                        'output': [],
                                        'cleanup': False,
                                        'usercache': [],
                                        'multiout': False
                                        }
            self.save_json()

    @checks.admin_or_permissions(Manage_server=True)
    @appset.command(name="reset", pass_context=True, no_pm=True)
    async def fix_cache(self, ctx):
        """Reset cache for applications"""
        server = ctx.message.server
        self.initial_config(ctx.message.server.id)
        self.settings[server.id]['usercache'] = []
        self.save_json()
        await self.bot.say("Cache has been reset")

    @checks.admin_or_permissions(Manage_server=True)
    @appset.command(name="roles", pass_context=True, no_pm=True)
    async def rolecreation(self, ctx):
        server = ctx.message.server
        author = ctx.message.author
        aprole = discord.utils.get(server, name="Staff Applicant")
        if aprole not in server.roles:
            await self.bot.create_role(server, name="Staff Applicant")
            await self.bot.say("All done!")
        else:
            await self.bot.say("Roles already present")

    @checks.admin_or_permissions(Manage_server=True)
    @appset.command(name="channel", pass_context=True, no_pm=True)
    async def setoutput(self, ctx, chan=None):
        """sets the place to output application embed to when finished."""
        server = ctx.message.server
        if server.id not in self.settings:
            self.initial_config(server.id)
        if chan in self.settings[server.id]['output']:
            return await self.bot.say("Channel already set as output")
        for channel in server.channels:
            if str(chan) == str(channel.id):
                if self.settings[server.id]['multiout']:
                    self.settings[server.id]['output'].append(chan)
                    self.save_json()
                    return await self.bot.say("Channel added to output list")
                else:
                    self.settings[server.id]['output'] = [chan]
                    self.save_json()
                    return await self.bot.say("Channel set as output")
        await self.bot.say("I could not find a channel with that id")

    @checks.admin_or_permissions(Manage_server=True)
    @appset.command(name="toggle", pass_context=True, no_pm=True)
    async def reg_toggle(self, ctx):
        """Toggles applications for the server"""
        server = ctx.message.server
        if server.id not in self.settings:
            self.initial_config(server.id)
        self.settings[server.id]['inactive'] = \
            not self.settings[server.id]['inactive']
        self.save_json()
        if self.settings[server.id]['inactive']:
            await self.bot.say("Registration disabled.")
        else:
            await self.bot.say("Registration enabled.")

    @commands.command(name="apply", pass_context=True)
    async def application(self, ctx):
        """"make an application by following the prompts"""
        author = ctx.message.author
        server = ctx.message.server
        aprole = discord.utils.get(server.roles, name="Staff Applicant")
        if server.id not in self.settings:
            return await self.bot.say("Applications are not setup on this server!")
        if self.settings[server.id]['inactive']:
            return await self.bot.say("We are not currently accepting applications, Try again later")
        if aprole in author.roles:
            await self.bot.say("{}You have already applied to this server!".format(author.mention))
        else:
            await self.bot.say("{}Ok lets start the application".format(author.mention))
            while True:
                avatar = author.avatar_url if author.avatar \
                    else author.default_avatar_url
                em = discord.Embed(timestamp=ctx.message.timestamp, title="ID: {}".format(author.id), color=discord.Color.blue())
                em.set_author(name='Staff Application for {}'.format(author.name), icon_url=avatar)
                agemsg = await self.bot.send_message(author, "What is your Age?")
                while True:
                    age = await self.bot.wait_for_message(channel=agemsg.channel, author=author, timeout=30)
                    if age is None:
                        await self.bot.send_message(author, "Sorry you took to long, please try again later!")
                        break
                    else:
                        em.add_field(name="Age: ", value=age.content, inline=True)
                        break
                if age is None:
                    break
                timemsg = await self.bot.send_message(author, "What TimeZone are you in? [Google is your Friend]")
                while True:
                    time = await self.bot.wait_for_message(channel=timemsg.channel, author=author, timeout=30)
                    if time is None:
                        await self.bot.send_message(author, "Timed out, Please run command again.")
                        break
                    else:
                        em.add_field(name="Timezone:", value=time.content, inline=True)
                        break
                if time is None:
                    break
                nationmsg = await self.bot.send_message(author, "What country are you from?")
                while True:
                    nation = await self.bot.wait_for_message(channel=nationmsg.channel, author=author, timeout=30)
                    if nation is None:
                        await self.bot.send_message(author, "Timed out Please run command again")
                        break
                    else:
                        em.add_field(name="Country: ", value=nation.content, inline=True)
                        em.add_field(name='Join Date', value=author.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
                        break
                if nation is None:
                    break
                activemsg = await self.bot.send_message(author, "How many hours per day can you be active?")
                while True:
                    active = await self.bot.wait_for_message(channel=activemsg.channel, author=author, timeout=60)
                    if active is None:
                        await self.bot.send_message(author, "Timed Out. Please re-run command and try again!")
                        break
                    else:
                        em.add_field(name="Active Hours per Day:", value=active.content, inline=False)
                        break
                if active is None:
                    break
                whymsg = await self.bot.send_message(author, "Why do you want to be staff?")
                while True:
                    why = await self.bot.wait_for_message(channel=whymsg.channel, author=author, timeout=60)
                    if why is None:
                        await self.bot.send_message(author, "Timed out, Please Re-Run command and try again!")
                        break
                    else:
                        em.add_field(name="Why do you want to be staff", value=why.content, inline=False)
                        aprole = discord.utils.get(server.roles, name="Applied")
                        await self.bot.add_roles(author, aprole)
                        await self.bot.send_message(author, "You have finished the application. Thank you")
                        break
                if why is None:
                    break
                for output in self.settings[server.id]['output']:
                    where = server.get_channel(output)
                    if where is not None:
                        await self.bot.send_message(where, embed=em)
                        break
                    break
                return

def check_folder():
    f = 'data/staffapp'
    if not os.path.exists(f):
        os.makedirs(f)


def check_file():
    f = 'data/staffapp/settings.json'
    if dataIO.is_valid_json(f) is False:
        dataIO.save_json(f, {})


def setup(bot):
    check_folder()
    check_file()
    n = staffapp(bot)
    bot.add_cog(n)
