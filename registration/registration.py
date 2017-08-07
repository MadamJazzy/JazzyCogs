import os
import asyncio  # noqa: F401
import discord
import logging
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from cogs.utils import checks

class registration:
    """Custom Cog for Intros"""
    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json('data/registration/settings.json')
        for s in self.settings:
            self.settings[s]['usercache'] = []
    def save_json(self):
        dataIO.save_json("data/registration/settings.json", self.settings)

    @commands.group(name="setreg", pass_context=True, no_pm=True)
    async def setreg(self, ctx):
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
    @setreg.command(name="reset", pass_context=True, no_pm=True)
    async def fix_cache(self, ctx):
        """Reset cache for registration"""
        server = ctx.message.server
        self.initial_config(ctx.message.server.id)
        self.settings[server.id]['usercache'] = []
        self.save_json()
        await self.bot.say("Cache has been reset")

    @checks.admin_or_permissions(Manage_server=True)
    @setreg.command(name="channel", pass_context=True, no_pm=True)
    async def setoutput(self, ctx, chan=None):
        """sets the place to output registration embed to when finished."""
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
    @setreg.command(name="toggle", pass_context=True, no_pm=True)
    async def reg_toggle(self, ctx):
        """Toggles registraton for the server"""
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

    @checks.admin_or_permissions(Manage_server=True)
    @setreg.command(name="roles", pass_context=True, no_pm=True)
    async def role_creation(self, ctx):
        """Creates roles needed for this cog"""
        server = ctx.message.server
        author = ctx.message.author
        try:
            rolemsg = await self.bot.reply("This will create the roles needed for this cog to function.\n```md\n"
                                       "[Gender Roles](Male, Female, Transgender)\n"
                                       "[Oritentation Roles](Straight, Gay, Bisexual, Pansexual)\n"
                                       "[Position Roles](Submissive, Dominant, Switch)\n"
                                       "[Misc Roles](Over 18, Registered)``` \n"
                                       "These roles are required for the cog to function correctly. They will be made "
                                       "with no permissions. You can modify this later through Role Management if you "
                                       "Need/Want to. Do you wish to continue? [This command will time out in 60s]")
            setrole = await self.bot.wait_for_message(channel=rolemsg.channel, author=author, timeout=60)
            if setrole.content.lower() == "no":
                await self.bot.reply("OK, Please create the required roles yourself before proceeding")
            elif setrole.content.lower() == "yes":
                await self.bot.reply("Ok, This will just take a moment")
                await self.bot.create_role(server, name="Male")
                await self.bot.create_role(server, name="Female")
                await self.bot.create_role(server, name="Transgender")
                await self.bot.create_role(server, name="Straight")
                await self.bot.create_role(server, name="Gay")
                await self.bot.create_role(server, name="Bisexual")
                await self.bot.create_role(server, name="Pansexual")
                await self.bot.create_role(server, name="Dominant")
                await self.bot.create_role(server, name="Submissive")
                await self.bot.create_role(server, name="Switch")
                await self.bot.create_role(server, name="Over 18")
                await self.bot.create_role(server, name="Registered")
                await asyncio.sleep(1.0)
                await self.bot.reply("All done!")
            else:
                await self.bot.reply("The command has timed out or you have entered an invalid response. "
                                     "Please only type yes or no. Try again later")
        except discord.HTTPException or discord.Forbidden:
            await self.bot.reply("Creation of roles has failed, The most common problem is that i do not Manage Roles "
                                 "Permissions on the server. Please check this and try again. or check your console! "
                                 "for full error details ")

    @commands.command(name="register", pass_context=True)
    async def registration(self, ctx):
        """"make a Introduction by following the prompts"""
        author = ctx.message.author
        server = ctx.message.server
        regrole = discord.utils.get(server.roles, name="Registered")
        if server.id not in self.settings:
            return await self.bot.say("Registrations have not been "
                                      "configured for this server.")
        if self.settings[server.id]['inactive']:
            return await self.bot.say("Registrations are not currently "
                                      "enabled on this server.")

        if regrole in author.roles:
            return await self.bot.say("You have already registered in this server.")
        else:
            await self.bot.say("{}I will DM you to collect your info. Please be honest and careful. This cannot be changed\n"
                               "Thank you!".format(author.mention))
        #Gather Intro Information
            while True:
                try:
                    avatar = author.avatar_url if author.avatar \
                        else author.default_avatar_url
                    em = discord.Embed(timestamp=ctx.message.timestamp, title="Registration {}".format(author.id),
                                       color=discord.Color.blue())
                    em.set_author(name='Introduction for {}'.format(author.name), icon_url=avatar)
                    gendermsg = await self.bot.send_message(author, "What is your Gender? Please choose from Male, "
                                                                    "Female, or Transgender.")
                    while True:
                        genders = ["male", "female", "transgender", "Male", "Female", "Transgender"]
                        gender = await self.bot.wait_for_message(channel=gendermsg.channel, author=author, timeout=60)
                        if gender is None:
                            await self.bot.send_message(author, "Registration has timed out. Please run register command again to continue!")
                            break
                        elif gender.content.lower() not in genders:
                            await self.bot.send_message(author,"You have chosen an incorrect response. Please choose Male, Female, or "
                                                               "Transgender. Make sure that you are spelling the choice correctly!")
                        elif gender.content.lower() in genders:
                            male = discord.utils.get(server.roles, name='Male')
                            female = discord.utils.get(server.roles, name='Female')
                            trans = discord.utils.get(server.roles, name='Transgender')
                            if gender.content.lower() == "male":
                                await self.bot.add_roles(author, male)
                                em.add_field(name="Gender", value="Male", inline=True)
                            elif gender.content.lower() == "female":
                                await self.bot.add_roles(author, female)
                                em.add_field(name="Gender", value="Female", inline=True)
                            else:
                                await self.bot.add_roles(author, trans)
                                em.add_field(name="Gender", value="Transgender", inline=True)
                            break
                    if gender is None:
                        break
                except discord.Forbidden:
                    await self.bot.reply("Sorry, You have your DMs disabled. I cannot register you if i cannot DM "
                                         "you. You are more than welcome to disable then again after we are done!")

                otmsg = await self.bot.send_message(author, "What is your Sexual Orientation? Please choose from Straight,"
                                                 " Bisexual, Pansexual, or Gay.")
                while True:
                    Orient = ["straight", "bisexual", "pansexual", "gay"]
                    ot = await self.bot.wait_for_message(channel=otmsg.channel, author=author, timeout=60)
                    if ot is None:
                        await self.bot.send_message(author, "Registration has timed out. Please run register command again to continue!")
                        break
                    elif ot.content.lower() not in Orient:
                        await self.bot.send_message(author, "You have entered an incorrect repsonse. Please choose from Straigh"
                                                            "t, Gay, Bisexual, or Pansexual. Remember to check your spelling!")
                    elif ot.content.lower() in Orient:
                        str8 = discord.utils.get(server.roles, name='Straight')
                        gay = discord.utils.get(server.roles, name='Gay')
                        bi = discord.utils.get(server.roles, name='Bisexual')
                        pan = discord.utils.get(server.roles, name='Pansexual')
                        if ot.content.lower() == "straight":
                            await self.bot.add_roles(author, str8)
                            em.add_field(name="Orientation", value="Straight", inline=True)
                        elif ot.content.lower() == "gay":
                            await self.bot.add_roles(author, gay)
                            em.add_field(name="Orientation", value="Gay", inline=True)
                        elif ot.content.lower() == "pansexual":
                            await self.bot.add_roles(author, pan)
                            em.add_field(name="Orientation", value="Pansexual", inline=True)
                        else:
                            await self.bot.add_roles(author, bi)
                            em.add_field(name="Orientation", value="Bisexual", inline=True)
                        break
                if ot is None:
                    break

                positionmsg = await self.bot.send_message(author, "Are you a Submissive, Dominant, or Switch?")
                while True:
                    pos = ["submissive", "dominant", "switch"]
                    position = await self.bot.wait_for_message(channel=positionmsg.channel, author=author, timeout=60)
                    if position is None:
                        await self.bot.send_message(author, "Registration has timed out. Please run register command again to continue!")
                        break
                    elif position.content.lower() not in pos:
                        await self.bot.send_message(author, "You have entered an incorrect response. Please choose from Submiss"
                                                            "ive, Dominant, or Switch. Remember to check your spelling!")
                    elif position.content.lower() in pos:
                        dom = discord.utils.get(server.roles, name='Dominant')
                        sub = discord.utils.get(server.roles, name='Submissive')
                        switch = discord.utils.get(server.roles, name='Switch')
                        if position.content.lower() == "dominant":
                            await self.bot.add_roles(author, dom)
                            em.add_field(name="Positon/Role", value="Dominant", inline=True)
                        elif position.content.lower() == "switch":
                            await self.bot.add_roles(author, switch)
                            em.add_field(name="Positon/Role", value="Switch", inline=True)
                        else:
                            await self.bot.add_roles(author, sub)
                            em.add_field(name="Positon/Role", value="Submissive", inline=True)
                        break
                if position is None:
                    break

                agemsg = await self.bot.send_message(author, "What is your Age? **BE TRUTHFUL** Lying will get your "
                                                             "account banned for 1 day, If you lie again after that "
                                                             "you will be **PERM BANNED**. Just tell the truth")
                while True:
                    over18 = discord.utils.get(server.roles, name="Over 18")
                    age = await self.bot.wait_for_message(channel=agemsg.channel, author=author, timeout=60)
                    if age is None:
                        break
                    else:
                        try:
                            if int(age.content) > 0:
                                if int(age.content) < 13:
                                    self.bot.kick(author)
                                elif int(age.content) >=18:
                                    await self.bot.add_roles(author, over18)
                                    em.add_field(name="Age", value=age.content, inline=True)
                                else:
                                    em.add_field(name="Age", value=age.content, inline=True)
                                break
                        except ValueError:
                            await self.bot.send_message(author, "Age must be a number. Try again. This field is required!")
                if age is None:
                    break
                aboutmemsg = await self.bot.send_message(author, "Tell us a little about yourself!")
                aboutme = await self.bot.wait_for_message(channel=aboutmemsg.channel, author=author, timeout=120)
                await self.bot.send_message(author, "Thank you, Registration is now complete!")
                if aboutme is not None:
                    em.add_field(name="About Me:", value=aboutme.content, inline=False)
                else:
                    em.add_field(name="About Me:", value="A mysterious person", inline=False)
                await self.bot.reply("Thank you for Registering!")
                await self.bot.add_roles(author, regrole)
                for output in self.settings[server.id]['output']:
                    where = server.get_channel(output)
                    if where is not None:
                        await self.bot.send_message(where, embed=em)
                        break
                else:
                    await self.bot.reply("Thank you for trying but Registration was **NOT** successful, One of your"
                                       "responses timed out. Please rerun the registration command to try again!"
                                         "You may not have all the roles that you should have.")
                    break
                return

def check_folder():
    f = 'data/registration'
    if not os.path.exists(f):
        os.makedirs(f)


def check_file():
    f = 'data/registration/settings.json'
    if dataIO.is_valid_json(f) is False:
        dataIO.save_json(f, {})


def setup(bot):
    check_folder()
    check_file()
    n = registration(bot)
    bot.add_cog(n)
