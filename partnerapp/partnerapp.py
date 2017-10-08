import os
import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from cogs.utils import checks


class partnerapp:
    """Custom Cog for applications"""
    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json('data/partner/settings.json')
        for s in self.settings:
            self.settings[s]['usercache'] = []
    def save_json(self):
        dataIO.save_json("data/partner/settings.json", self.settings)

    @commands.group(name="pset", pass_context=True, no_pm=True)
    async def pset(self, ctx):
        """configuration settings"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
    def initial_config(self, server_id):
        """makes an entry for the server, defaults to turned off"""
        if server_id not in self.settings:
            self.settings[server_id] = {'inactive': True,
                                        'output': [],
                                        'usercache': [],
                                        'usermin': 0,
                                        'partnermsg': [],
                                        'multiout': False
                                        }
            self.save_json()

    @checks.admin_or_permissions(Manage_server=True)
    @pset.command(name="roles", pass_context=True, no_pm=True)
    async def rolecreation(self, ctx):
        author = ctx.message.author
        server = ctx.message.server
        aprole = discord.utils.get(server.roles, name="Partner Applicant")
        partnerrole = discord.utils.get(server.roles, name="Partners")
        if partnerrole not in server.roles:
            await self.bot.create_role(server, name="Partners")
        if aprole not in server.roles:
            await self.bot.create_role(server, name="Partner Applicant")
        await self.bot.say("All done!")


    @checks.admin_or_permissions(Manage_server=True)
    @pset.command(name="msg", pass_context=True, no_pm=True)
    async def pmsg(self, ctx,):
        """Set your servers Partner message"""
        server = ctx.message.server
        author = ctx.message.author
        msg = await self.bot.say("Please enter your Parter message, Do not include code blocks as they will be added"
                                 "by the bot later")
        pmsg = await self.bot.wait_for_message(channel=msg.channel, author=author, timeout=120)
        if pmsg is not None:
            try:
                if server.id not in self.settings:
                    self.initial_config(server.id)
                else:
                    self.settings[server.id]['partnermsg'] = [pmsg]
                    self.save_json()
                    await self.bot.say("Partner Message has been set")
            except AttributeError:
                pass
        else:
            await self.bot.say("You must enter a partner message. Do not include quotes or block text")

    @checks.admin_or_permissions(Manage_server=True)
    @pset.command(name="channel", pass_context=True, no_pm=True)
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
    @pset.command(name="usermin", pass_context=True, no_pm=True)
    async def usermin(self, ctx, usermin=0):
        """set a min number of users a server must have to apply"""
        server = ctx.message.server
        author = ctx.message.author
        if usermin >= 0:
            if server.id not in self.settings:
                self.initial_config(server.id)
            else:
                self.settings[server.id]['usermin'] = usermin
                self.save_json()
                await self.bot.say("{} has been set as min number of users".format(usermin))
        else:
            await self.bot.say("{} Input must be a number please try again".format(author.mention))

    @checks.admin_or_permissions(Manage_server=True)
    @pset.command(name="toggle", pass_context=True, no_pm=True)
    async def reg_toggle(self, ctx):
        """Toggles applications for the server"""
        server = ctx.message.server
        if server.id not in self.settings:
            self.initial_config(server.id)
        self.settings[server.id]['inactive'] = \
            not self.settings[server.id]['inactive']
        self.save_json()
        if self.settings[server.id]['inactive']:
            await self.bot.say("Partner Applications disabled.")
        else:
            await self.bot.say("Partner Applications enabled.")

    @commands.command(name="partner", pass_context=True)
    async def application(self, ctx,):
        """"make an application by following the prompts"""
        author = ctx.message.author
        server = ctx.message.server
        aprole = discord.utils.get(server.roles, name="Partner Applicant")
        partnerrole = discord.utils.get(server.roles, name="Partners")
        usermin = self.settings[server.id]['usermin']
        pmsg = self.settings[server.id]['partnermsg']
        if server.id not in self.settings:
            return await self.bot.say("Partner Applications are not setup on this server!")
        if self.settings[server.id]['inactive']:
            return await self.bot.say("We are not currently accepting partnership applications, Try again later")
        if partnerrole in author.roles:
            await self.bot.say("{}, You have already partnered with this server!".format(author.mention))
        elif aprole in author.roles:
            await self.bot.say("{}, You have already applied for partnership on this server!".format(author.mention))
        else:
            await self.bot.say("{}, Ok I will DM you to start the application!".format(author.name))
            while True:
                avatar = author.avatar_url if author.avatar \
                    else author.default_avatar_url
                em = discord.Embed(timestamp=ctx.message.timestamp, title="ID: {}".format(author.id), color=discord.Color.blue())
                em.set_author(name='Partnership Application for {}'.format(author.name), icon_url=avatar)
                try:
                    membermsg = await self.bot.send_message(author, "How many members does your server have. "
                                                                    "Please only put the number, do not include anything"
                                                                    "but numbers in this response or you will get an error"
                                                                    "Example:1214 is acceptable 1000+ is **NOT**")
                    while True:
                        member = await self.bot.wait_for_message(channel=membermsg.channel, author=author, timeout=30)
                        member1 = int(member.content)
                        if member is None:
                            await self.bot.send_message(author, "Sorry you took to long, please try again!")
                            break
                        else:
                            try:
                                member1 = int(member.content)
                                if member1 > 0:
                                    if member1 < usermin:
                                        await self.bot.send_message(author, "You do not meet our member guidelines for "
                                                                            "parternship at this time. You must have "
                                                                            "no less than {} members in your server!"
                                                                            "".format(usermin))
                                        break
                                    elif member1 >= usermin:
                                        em.add_field(name="MemberCount: ", value=member.content, inline=True)
                                        break
                                else:
                                    await self.bot.send_message(author, "You have entered an invalid response. "
                                                                        "Please only use positve numbers and no + signs "
                                                                        "Number only. Example: 1524 and not 1500+ ")
                                    break
                            except ValueError or AttributeError:
                                await self.bot.send_message(author, "Member count must be a number, try again do not "
                                                                    "include any symbols like + or - ")
                                break
                    if member is None:
                        break
                    elif member1 < usermin:
                        break
                except discord.Forbidden:
                    await self.bot.reply("You have your DMs turned off. I cannot DM you. Please enable your DMs to "
                                         "continue. You can turn them back off after we are done.")
                    pass
                    break

                namemsg = await self.bot.send_message(author, "What is your Server's Name?")
                while True:
                    name = await self.bot.wait_for_message(channel=namemsg.channel, author=author, timeout=30)
                    if name is None:
                        await self.bot.send_message(author, "Entry timed  out, Please try again by running the command"
                                                            "again. The bot waits for 30 seconds on this question.")
                        break
                    else:
                        em.add_field(name="Server Name:", value=name.content, inline=True)
                        break
                if name is None:
                    break
                ownermsg = await self.bot.send_message(author, "Who is the Owner of this Server? Example Owner#1234"
                                                               "Be sure to include the full name and discrim.")
                while True:
                    owner = await self.bot.wait_for_message(channel=ownermsg.channel, author=author, timeout=45)
                    if owner is None:
                        await self.bot.send_message(author, "Entry has timed out, Please start over and try again")
                        break
                    else:
                        em.add_field(name="Server Owner:", value=owner.content, inline=True)
                        break
                if owner is None:
                    break

                typemsg = await self.bot.send_message(author, "What type of server is this? Examples include:"
                                                              " Community, Gaming, Bot, Adult, Dating. ect.")
                while True:
                    type = await self.bot.wait_for_message(channel=typemsg.channel, author=author, timeout=30)
                    if type is None:
                        await self.bot.send_message(author, "Command has timed out. Please rerun the command to try again")
                        break
                    else:
                        em.add_field(name="Server Type:", value=type.content, inline=True)
                        break
                if type is None:
                    break

                linkmsg = await self.bot.send_message(author, "What is your Invite link? This must be a discord.gg/INVITE "
                                                              "type of link. Please make sure that this link is set to "
                                                              "not expire.")
                while True:
                    link = await self.bot.wait_for_message(channel=linkmsg.channel, author=author, timeout=30)
                    if link is None:
                        await self.bot.send_message(author, "Timed out, Please run command again.")
                        break
                    else:
                        em.add_field(name="Invite Link: ", value=link.content, inline=True)
                        break
                if link is None:
                    break
                infomsg = await self.bot.send_message(author, "Please provide us with a short description of your server "
                                                              "this will be what is posted in the partners channel if your "
                                                              "application gets approved. Please make sure to perfect "
                                                              "your description formatting BEFORE sending it here. "
                                                              "If you need to change it later speak to a staff member! "
                                                              "You have 2 Mins to write your info. Otherwise the "
                                                              "application will time out and you will have to start over!")
                while True:
                    info = await self.bot.wait_for_message(channel=infomsg.channel, author=author, timeout=120)
                    if info is None:
                        await self.bot.send_message(author, "Timed out Please run command again")
                        break
                    else:
                        em.add_field(name="Partner Message:", value="```" + info.content + "```", inline=False)
                        break
                aprole = discord.utils.get(server.roles, name="Partner Applicant")
                if self.settings[server.id]['partnermsg'] is not None:
                    await self.bot.send_message(author, "Our Partnership message is ...")
                    await self.bot.send_message(author, "``` {} ```".format(pmsg.content))
                    await self.bot.send_message(author, "You have completed the application process, your application "
                                                        "has been submitted to the partner request queue and a member"
                                                        "of staff will be with you asap.")
                else:
                    await self.bot.send_message(author, "You have completed the application process, your application "
                                                        "has been submitted to the partner request queue and a member"
                                                        "of staff will be with you asap.")
                for output in self.settings[server.id]['output']:
                    where = server.get_channel(output)
                    if where is not None:
                        if member1 < usermin:
                            await self.bot.send_message(author, "You do not meet our member guidelines for "
                                                                "parternship at this time. You must have "
                                                                "no less than {} members in your server!".format(usermin))
                        else:
                            await self.bot.send_message(where, embed=em)
                            await self.bot.send_message(where, "Partner Message for {}".format(author.mention))
                            await self.bot.add_roles(author, aprole)
                            break
                        break

                    break
                return


def check_folder():
    f = 'data/partner'
    if not os.path.exists(f):
        os.makedirs(f)


def check_file():
    f = 'data/partner/settings.json'
    if dataIO.is_valid_json(f) is False:
        dataIO.save_json(f, {})


def setup(bot):
    check_folder()
    check_file()
    n = partnerapp(bot)
    bot.add_cog(n)
