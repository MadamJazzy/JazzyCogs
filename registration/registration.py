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
                                       "[Gender Roles](Male, Female, Transgender, MTF, and FTM)\n"
                                       "[Oritentation Roles](Straight, Gay, Bisexual, Pansexual, and Asexual)\n"
                                       "[Position Roles](Submissive, Dominant, Switch)\n"
                                       "[Misc Roles](Over 18, Registered, Under 18)``` \n"
                                       "These roles are required for the cog to function correctly. They will be made "
                                       "with no permissions. You can modify this later through Role Management if you "
                                       "Need/Want to. Do you wish to continue? [This command will time out in 60s]")
            setrole = await self.bot.wait_for_message(channel=rolemsg.channel, author=author, timeout=60)
            if setrole.content.lower() == "no":
                await self.bot.reply("OK, This must be done before the command will work correctly!")
            elif setrole.content.lower() == "yes":
                male = discord.utils.get(server.roles, name="Male")
                female = discord.utils.get(server.roles, name="Female")
                trans = discord.utils.get(server.roles, name="Transgender")
                mtf = discord.utils.get(server.roles, name="Trans MTF")
                ftm = discord.utils.get(server.roles, name="Trans FTM")
                str8 = discord.utils.get(server.roles, name="Straight")
                gay = discord.utils.get(server.roles, name="Gay")
                bi = discord.utils.get(server.roles, name="Bisexual")
                pan = discord.utils.get(server.roles, name="Pansexual")
                asexual = discord.utils.get(server.roles, name="Asexual")
                dom = discord.utils.get(server.roles, name="Dominant")
                sub = discord.utils.get(server.roles, name="Submissive")
                switch = discord.utils.get(server.roles, name="Switch")
                reg = discord.utils.get(server.roles, name="Registered")
                over = discord.utils.get(server.roles, name="Over 18")
                under = discord.utils.get(server.roles, name="Under 18")

                await self.bot.reply("Ok, This will just take a moment")
                if male not in server.roles:
                    await self.bot.create_role(server, name="Male")
                if female not in server.roles:
                    await self.bot.create_role(server, name="Female")
                if trans not in server.roles:
                    await self.bot.create_role(server, name="Transgender")
                if str8 not in server.roles:
                    await self.bot.create_role(server, name="Straight")
                if gay not in server.roles:
                    await self.bot.create_role(server, name="Gay")
                if bi not in server.roles:
                    await self.bot.create_role(server, name="Bisexual")
                if pan not in server.roles:
                    await self.bot.create_role(server, name="Pansexual")
                if dom not in server.roles:
                    await self.bot.create_role(server, name="Dominant")
                if sub not in server.roles:
                    await self.bot.create_role(server, name="Submissive")
                if switch not in server.roles:
                    await self.bot.create_role(server, name="Switch")
                if over not in server.roles:
                    await self.bot.create_role(server, name="Over 18")
                if reg not in server.roles:
                    await self.bot.create_role(server, name="Registered")
                if under not in server.roles:
                    await self.bot.create_role(server, name="Under 18")
                if mtf not in server.roles:
                    await self.bot.create_role(server, name="Trans MTF")
                if ftm not in server.roles:
                    await self.bot.create_role(server, name="Trans FTM")
                if asexual not in server.roles:
                    await self.bot.create_role(server, name="Asexual")
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
                        genders = ["male", "female", "trans", "trans mtf", "trans ftm"]
                        gender = await self.bot.wait_for_message(channel=gendermsg.channel, author=author, timeout=60)
                        if gender is None:
                            await self.bot.send_message(author, "Registration has timed out. Please run register command again to continue!")
                            break
                        elif gender.content.lower() not in genders:
                            await self.bot.send_message(author,"You have chosen an incorrect response. Please choose Male, Female, "
                                                               "Trans, Trans MTF, or Trans FTM. Make sure that you are spelling the choice correctly!")
                        elif gender.content.lower() in genders:
                            male = discord.utils.get(server.roles, name='Male')
                            female = discord.utils.get(server.roles, name='Female')
                            trans = discord.utils.get(server.roles, name='Transgender')
                            mtf = discord.utils.get(server.roles, name="Trans MTF")
                            ftm = discord.utils.get(server.roles, name="Trans FTM")
                            if gender.content.lower() == "male":
                                await self.bot.add_roles(author, male)
                                em.add_field(name="Gender", value="Male", inline=True)
                            elif gender.content.lower() == "female":
                                await self.bot.add_roles(author, female)
                                em.add_field(name="Gender", value="Female", inline=True)
                            elif gender.content.lower() == "trans mtf":
                                await self.bot.add_roles(author, mtf)
                                em.add_field(name="Gender", value="Trans MTF", inline=True)
                            elif gender.content.lower() == "trans ftm":
                                await self.bot.add_roles(author, ftm)
                                em.add_field(name="Gender", value="Trans FTM", inline=True)
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
                                                 " Bisexual, Pansexual, Asexual, or Gay.")
                while True:
                    Orient = ["straight", "bisexual", "pansexual", "gay", "asexual"]
                    ot = await self.bot.wait_for_message(channel=otmsg.channel, author=author, timeout=60)
                    if ot is None:
                        await self.bot.send_message(author, "Registration has timed out. Please run register command again to continue!")
                        break
                    elif ot.content.lower() not in Orient:
                        await self.bot.send_message(author, "You have entered an incorrect repsonse. Please choose from Straigh"
                                                            "t, Gay, Bisexual, Asexual, or Pansexual. Remember to check your spelling!")
                    elif ot.content.lower() in Orient:
                        str8 = discord.utils.get(server.roles, name='Straight')
                        gay = discord.utils.get(server.roles, name='Gay')
                        bi = discord.utils.get(server.roles, name='Bisexual')
                        pan = discord.utils.get(server.roles, name='Pansexual')
                        asexual = discord.utils.get(server.roles, name="Asexual")
                        if ot.content.lower() == "straight":
                            await self.bot.add_roles(author, str8)
                            em.add_field(name="Orientation", value="Straight", inline=True)
                        elif ot.content.lower() == "gay":
                            await self.bot.add_roles(author, gay)
                            em.add_field(name="Orientation", value="Gay", inline=True)
                        elif ot.content.lower() == "pansexual":
                            await self.bot.add_roles(author, pan)
                            em.add_field(name="Orientation", value="Pansexual", inline=True)
                        elif ot.content.lower() == "asexual":
                            await self.bot.add_roles(author, asexual)
                            em.add_field(name="Orientation", value="Asexual", inline=True)
                        else:
                            await self.bot.add_roles(author, bi)
                            em.add_field(name="Orientation", value="Bisexual", inline=True)
                        break
                if ot is None:
                    break

                positionmsg = await self.bot.send_message(author, "Are you a Submissive, Dominant, or Switch?\n"
                                                                  "```Explination```\n:one:Submissive - This means you "
                                                                  "are passive and not aggressive in relationships\n"
                                                                  ":two:Dominant - This means you are aggressive in "
                                                                  "relationships\n:three:Switch - This means you are "
                                                                  "both passive and aggressive or you 'switch' roles "
                                                                  "in relationships.")
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

                agemsg = await self.bot.send_message(author, "What is your Age? **BE TRUTHFUL** Lying will most likely "
                                                             "result in consequences by admins, owners of the server! Just"
                                                             "be honest")
                while True:
                    over18 = discord.utils.get(server.roles, name="Over 18")
                    age = await self.bot.wait_for_message(channel=agemsg.channel, author=author, timeout=60)
                    if age is None:
                        break
                    else:
                        try:
                            if int(age.content) > 0:
                                if int(age.content) < 13:
                                    await self.bot.send_message(author, "Children under the age of 13 are not allowed"
                                                                        "to be on the discord platform. You have been"
                                                                        "kicked from this server. If you attempt to "
                                                                        "rejoin you will be banned and reported to "
                                                                        "discord.\nthank you")
                                    self.bot.kick(author)
                                elif int(age.content) >=18:
                                    await self.bot.add_roles(author, over18)
                                    em.add_field(name="Age", value=age.content, inline=True)
                                else:
                                    under = discord.utils.get(server.roles, name="Under 18")
                                    em.add_field(name="Age", value=age.content, inline=True)
                                    await self.bot.add_roles(author, under)
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
