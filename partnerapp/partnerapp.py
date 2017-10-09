import os
import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from cogs.utils import checks
import rethinkdb as r

r.connect('localhost', 28015, db="partner").repl()


class partnerapp:
    """Custom Cog for applications"""

    def __init__(self, bot):
        self.bot = bot

    def get_app(self, server_id):
        try:
            return r.table("apps").get(str(server_id)).run()
        except:
            return None

    def get_settings(self, server_id):
        try:
            return r.table("settings").get(str(server_id)).run()
        except:
            return None

    def save_app(self, app):
        try:
            r.table("apps").insert(app, conflict="update").run()
        except:
            pass

    def save_settings(self, setting):
        try:
            r.table("settings").insert(setting, conflict="update").run()
        except:
            pass

    def initial_config(self, server_id):
        try:
            r.table_create("settings").run()
        except:
            pass
        try:
            r.table_create("apps").run()
        except:
            pass
        self.save_settings({"id": server_id,
                            "inactive": True,
                            "usermin": 0,
                            "message": 0})

    @commands.group(name="pset", pass_context=True, no_pm=True)
    async def pset(self, ctx):
        """configuration settings"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @checks.admin_or_permissions(Manage_server=True)
    @pset.command(name="msg", pass_context=True, no_pm=True)
    async def pmsg(self, ctx, ):
        """Set your servers Partner message"""
        server = ctx.message.server
        author = ctx.message.author
        setting = self.get_settings(str(server.id))
        msg = await self.bot.say("Please enter your Parter message, Do not include code blocks as they will be added"
                                 "by the bot later")
        pmsg = await self.bot.wait_for_message(channel=msg.channel, author=author, timeout=120)
        if pmsg is not None:
            try:
                if setting is not None:
                    setting["message"] = pmsg
                    self.save_settings(setting)
                    await self.bot.say("Partner Message has been set.")
                else:
                    self.initial_config(str(server.id))
            except AttributeError:
                pass
        else:
            await self.bot.say("You must enter a partner message. Do not include quotes or block text")

    @checks.admin_or_permissions(Manage_server=True)
    @pset.command(name="channel", pass_context=True, no_pm=True)
    async def setoutput(self, ctx, chan=None):
        """sets the place to output application embed to when finished."""
        server = ctx.message.server
        setting = self.get_settings(str(server.id))
        if chan is not None:
            try:
                if setting is not None:
                    setting["channel"] = chan
                    self.save_settings(setting)
                    await self.bot.say("The <#{}> will be used to post applications!".format(chan))
                else:
                    self.initial_config(str(server.id))
            except AttributeError:
                pass

    @checks.admin_or_permissions(Manage_server=True)
    @pset.command(name="usermin", pass_context=True, no_pm=True)
    async def usermin(self, ctx, usermin=0):
        """set a min number of users a server must have to apply"""
        server = ctx.message.server
        author = ctx.message.author
        setting = self.get_settings(str(server.id))
        if usermin >= 0:
            if setting is not None:
                setting["usermin"] = usermin
                self.save_settings(setting)
                await self.bot.say("{} has been set as min number of users".format(usermin))
            else:
                self.initial_config(str(server.id))
        else:
            await self.bot.say("{} Input must be a number please try again".format(author.mention))

    @checks.admin_or_permissions(Manage_server=True)
    @pset.command(name="toggle", pass_context=True, no_pm=True)
    async def reg_toggle(self, ctx):
        """Toggles applications for the server"""
        server = ctx.message.server
        setting = self.get_settings(str(server.id))
        if setting is not None:
            setting["inactive"] = \
            self.save_settings(setting)
        if setting['inactive'] is False:
            await self.bot.say("Partner Applications disabled.")
        else:
            await self.bot.say("Partner Applications enabled.")

    @commands.command(name="partner", pass_context=True)
    async def application(self, ctx,):
        """"make an application by following the prompts"""
        author = ctx.message.author
        server = ctx.message.server
        usermin = r.table('settings').get(server.id)["usermin"]
        pmsg = r.table('settings').get(server.id)["partnermsg"]
        setting = self.get_settings(str(server.id))
        app = self.get_app(str(server.id))
        if setting is None:
            return await self.bot.say("Partner Applications are not setup on this server!")
        if setting["inactive"] is True:
            return await self.bot.say("We are not currently accepting partnership applications, Try again later")
        if app["pid"] is True:
            await self.bot.say("{}, You have already applied to this server!".format(author.mention))
            await self.bot.say("You application was {}".format(app["status"]))
        else:
            await self.bot.say("{}, Ok I will DM you to start the application! For this application you "
                               "will need to have your Server ID, Server Name, Owner Name, Number of Members "
                               "Perm Invite link, and your servers partner message. ".format(author.name))


            while True:
                avatar = author.avatar_url if author.avatar \
                    else author.default_avatar_url
                em = discord.Embed(timestamp=ctx.message.timestamp, title="ID: {}".format(author.id), color=discord.Color.blue())
                em.set_author(name='Partnership Application for {}'.format(author.name), icon_url=avatar)
                try:
                    idmsg = await self.bot.send_message(author, "What is your servers ID? You can obtain this by doing "
                                                                "serverinfo on almost any bot. If you need help contant a "
                                                                "staff member. if this number is not correct then the "
                                                                "application cannot be approved.")
                    while True:
                        id = await self.bot.wait_for_message(channel=idmsg.channel, author=author, timeout=30)
                        if id is None:
                            await self.bot.send_message(author, "Sorry you took to long, Try again later")
                            break
                        else:
                            try:
                                em.add_field(name="Server ID", value=id.content, inline=True)
                            except AttributeError:
                                pass
                    if id is None:
                        break
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
                                        app["members"] = member1
                                        self.save_app(app)
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
                idmsg = await self.bot.send_message(author, "What is your Server ID? (You can get this by doing serverinfo"
                                                            "command on almost any bot.")

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
                if self.get_settings(setting)["message"] is not None:
                    await self.bot.send_message(author, "Our Partnership message is ...")
                    await self.bot.send_message(author, "``` {} ```".format(pmsg))
                    await self.bot.send_message(author, "You have completed the application process, your application "
                                                        "has been submitted to the partner request queue and a member"
                                                        "of staff will be with you asap.")
                else:
                    await self.bot.send_message(author, "You have completed the application process, your application "
                                                        "has been submitted to the partner request queue and a member"
                                                        "of staff will be with you asap.")
                for channel in r.table('settings').get(server.id)["channel"]:
                    where = server.get_channel(channel)
                    if where is not None:
                        if member1 < usermin:
                            await self.bot.send_message(author, "You do not meet our member guidelines for "
                                                                "parternship at this time. You must have "
                                                                "no less than {} members in your server!".format(usermin))
                        else:
                            await self.bot.send_message(where, embed=em)
                            await self.bot.send_message(where, "Partner Message for {}".format(author.mention))
                            await self.bot.add_roles(author, aprole)
                            appid = server.id + "-" + id.content
                            self.save_app({"id": appid,
                                           "pid": id.content,
                                           "servername": name.content,
                                           "userid": author.id,
                                           "username": author.name,
                                           "members": member.content,
                                           "invite": link.content,
                                           "info": info.content,
                                           "status": "Pending"
                                           })

                            break
                        break

                    break
                return

    @commands.group(name="pmod", pass_context=True, no_pm=True)
    async def pmod(self, ctx):
        """Moderate the Partner Applications"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
    @checks.mod_or_permissions(ManageMessages=True)
    @pmod.command(name="approve", pass_context=True, no_pm=True)
    async def approve(self, ctx, id=None):
        server = ctx.message.server
        appid = server.id + "-" + id.content
        app = self.get_app(str(appid))
        if app is True:
            app["status"] = "Approved"
            self.save_app(app)
        else:
            await self.bot.say("Ooops, This does not seem to be a valid Application ID, Make sure you are using the "
                               "Server ID that they entered when they applied")

    @checks.mod_or_permissions(ManageMessages=True)
    @pmod.command(name="deny", pass_context=True, no_pm=True)
    async def deny(self, ctx, id=None):
        server = ctx.message.server
        appid = server.id + "-" + id.content
        app = self.get_app(str(appid))
        if app is True:
            app["status"] = "Denied"
            self.save_app(app)
        else:
            await self.bot.say("Ooops, This does not seem to be a valid Application ID, Make sure you are using the "
                               "Server ID that they entered when they applied")

def setup(bot):
    n = partnerapp(bot)
    bot.add_cog(n)
