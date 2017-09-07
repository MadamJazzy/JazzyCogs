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
                                           "[Orientation Roles](Straight, Gay, Bisexual, Pansexual, and Asexual)\n"
                                           "[Position Roles](Submissive, Dominant, Switch)\n"
                                           "[Misc Roles](Over 18, Registered, Under 18) \n"
                                           "[Location Roles](52 location roles)```\n"
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
                usa1 = discord.utils.get(server.roles, name="USA-Eastern")
                usa2 = discord.utils.get(server.roles, name="USA-Central")
                usa3 = discord.utils.get(server.roles, name="USA-Pacific")
                usa4 = discord.utils.get(server.roles, name="USA-Mountain")
                africa = discord.utils.get(server.roles, name="Africa")
                asia = discord.utils.get(server.roles, name="Asia")
                australia = discord.utils.get(server.roles, name="Australia")
                austria = discord.utils.get(server.roles, name="Austria")
                belgium = discord.utils.get(server.roles, name="Belgium")
                bosnia = discord.utils.get(server.roles, name="Bosnia")
                brazil = discord.utils.get(server.roles, name="Brazil")
                bulgaria = discord.utils.get(server.roles, name="Bulgaria")
                canada = discord.utils.get(server.roles, name="Canada")
                croatia = discord.utils.get(server.roles, name="Croatia")
                czech = discord.utils.get(server.roles, name="Czech")
                denmark = discord.utils.get(server.roles, name="Denmark")
                estonia = discord.utils.get(server.roles, name="Estonia")
                europe = discord.utils.get(server.roles, name="Europe")
                finland = discord.utils.get(server.roles, name="Finland")
                france = discord.utils.get(server.roles, name="France")
                germany = discord.utils.get(server.roles, name="Germany")
                hungary = discord.utils.get(server.roles, name="Hungary")
                ireland = discord.utils.get(server.roles, name="Ireland")
                israel = discord.utils.get(server.roles, name="Israel")
                italy = discord.utils.get(server.roles, name="Italy")
                latvia = discord.utils.get(server.roles, name="Latvia")
                lithuania = discord.utils.get(server.roles, name="Lithuania")
                macedonia = discord.utils.get(server.roles, name="Macedonia")
                mexico = discord.utils.get(server.roles, name="Mexico")
                middleeast = discord.utils.get(server.roles, name="Middle East")
                netherlands = discord.utils.get(server.roles, name="Netherlands")
                norway = discord.utils.get(server.roles, name="Norway")
                newzealand = discord.utils.get(server.roles, name="New Zealand")
                philippines = discord.utils.get(server.roles, name="Philippines")
                poland = discord.utils.get(server.roles, name="Poland")
                portugal = discord.utils.get(server.roles, name="Portugal")
                romania = discord.utils.get(server.roles, name="Romania")
                russia = discord.utils.get(server.roles, name="Russia")
                saudi = discord.utils.get(server.roles, name="Saudi")
                scotland = discord.utils.get(server.roles, name="Scotland")
                serbia = discord.utils.get(server.roles, name="Serbia")
                singapore = discord.utils.get(server.roles, name="Singapore")
                slovakia = discord.utils.get(server.roles, name="Slovakia")
                slovenia = discord.utils.get(server.roles, name="Slovenia")
                southamerica = discord.utils.get(server.roles, name="South America")
                spain = discord.utils.get(server.roles, name="Spain")
                sweden = discord.utils.get(server.roles, name="Sweden")
                switzerland = discord.utils.get(server.roles, name="Switzerland")
                turkey = discord.utils.get(server.roles, name="Turkey")
                uk = discord.utils.get(server.roles, name="United Kingdom")

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
                if usa1 not in server.roles:
                    await self.bot.create_role(server, name="USA-Eastern")
                if usa2 not in server.roles:
                    await self.bot.create_role(server, name="USA-Central")
                if usa3 not in server.roles:
                    await self.bot.create_role(server, name="USA-Pacific")
                if usa4 not in server.roles:
                    await self.bot.create_role(server, name="USA-Mountain")
                if africa not in server.roles:
                    await self.bot.create_role(server, name="Africa")
                if asia not in server.roles:
                    await self.bot.create_role(server, name="Asia")
                if australia not in server.roles:
                    await self.bot.create_role(server, name="Australia")
                if austria not in server.roles:
                    await self.bot.create_role(server, name="Austria")
                if belgium not in server.roles:
                    await self.bot.create_role(server, name="Belgium")
                if bosnia not in server.roles:
                    await self.bot.create_role(server, name="Bosnia")
                if brazil not in server.roles:
                    await self.bot.create_role(server, name="Brazil")
                if bulgaria not in server.roles:
                    await self.bot.create_role(server, name="Bulgaria")
                if canada not in server.roles:
                    await self.bot.create_role(server, name="Canada")
                if croatia not in server.roles:
                    await self.bot.create_role(server, name="Croatia")
                if czech not in server.roles:
                    await self.bot.create_role(server, name="Czech")
                if denmark not in server.roles:
                    await self.bot.create_role(server, name="Denmark")
                if estonia not in server.roles:
                    await self.bot.create_role(server, name="Estonia")
                if europe not in server.roles:
                    await self.bot.create_role(server, name="Europe")
                if finland not in server.roles:
                    await self.bot.create_role(server, name="Finland")
                if france not in server.roles:
                    await self.bot.create_role(server, name="France")
                if germany not in server.roles:
                    await self.bot.create_role(server, name="Germany")
                if hungary not in server.roles:
                    await self.bot.create_role(server, name="Hungary")
                if ireland not in server.roles:
                    await self.bot.create_role(server, name="Ireland")
                if israel not in server.roles:
                    await self.bot.create_role(server, name="Israel")
                if italy not in server.roles:
                    await self.bot.create_role(server, name="Italy")
                if latvia not in server.roles:
                    await self.bot.create_role(server, name="Latvia")
                if lithuania not in server.roles:
                    await self.bot.create_role(server, name="Lithuania")
                if macedonia not in server.roles:
                    await self.bot.create_role(server, name="Macedonia")
                if mexico not in server.roles:
                    await self.bot.create_role(server, name="Mexico")
                if middleeast not in server.roles:
                    await self.bot.create_role(server, name="Middle East")
                if netherlands not in server.roles:
                    await self.bot.create_role(server, name="Netherlands")
                if norway not in server.roles:
                    await self.bot.create_role(server, name="Norway")
                if newzealand not in server.roles:
                    await self.bot.create_role(server, name="New Zealand")
                if philippines not in server.roles:
                    await self.bot.create_role(server, name="Philippines")
                if poland not in server.roles:
                    await self.bot.create_role(server, name="Poland")
                if portugal not in server.roles:
                    await self.bot.create_role(server, name="Portugal")
                await asyncio.sleep(2.0)
                if romania not in server.roles:
                    await self.bot.create_role(server, name="Romania")
                if russia not in server.roles:
                    await self.bot.create_role(server, name="Russia")
                if saudi not in server.roles:
                    await self.bot.create_role(server, name="Saudi")
                if scotland not in server.roles:
                    await self.bot.create_role(server, name="Scotland")
                if serbia not in server.roles:
                    await self.bot.create_role(server, name="Serbia")
                if singapore not in server.roles:
                    await self.bot.create_role(server, name="Singapore")
                if slovakia not in server.roles:
                    await self.bot.create_role(server, name="Slovakia")
                if slovenia not in server.roles:
                    await self.bot.create_role(server, name="Slovenia")
                if southamerica not in server.roles:
                    await self.bot.create_role(server, name="South America")
                if spain not in server.roles:
                    await self.bot.create_role(server, name="Spain")
                if sweden not in server.roles:
                    await self.bot.create_role(server, name="Sweden")
                if switzerland not in server.roles:
                    await self.bot.create_role(server, name="Switzerland")
                if turkey not in server.roles:
                    await self.bot.create_role(server, name="Turkey")
                if uk not in server.roles:
                    await self.bot.create_role(server, name="United Kingdom")
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
            await self.bot.say(
                "{}I will DM you to collect your info. Please be honest and careful. This cannot be changed\n"
                "Thank you!".format(author.mention))
            # Gather Intro Information
            while True:
                try:
                    avatar = author.avatar_url if author.avatar \
                        else author.default_avatar_url
                    em = discord.Embed(timestamp=ctx.message.timestamp, title="Registration {}".format(author.id),
                                       color=discord.Color.blue())
                    em.set_author(name='Introduction for {}'.format(author.name), icon_url=avatar)
                    gendermsg = await self.bot.send_message(author, "What is your Gender? Please choose from Male, "
                                                                    "Female, Trans, Trans MTF, or Trans FTM")
                    while True:
                        genders = ["male", "female", "trans", "trans mtf", "trans ftm"]
                        gender = await self.bot.wait_for_message(channel=gendermsg.channel, author=author, timeout=60)
                        if gender is None:
                            await self.bot.send_message(author,
                                                        "Registration has timed out. Please run register command again to continue!")
                            break
                        elif gender.content.lower() not in genders:
                            await self.bot.send_message(author,
                                                        "You have chosen an incorrect response. Please choose Male, Female, "
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

                otmsg = await self.bot.send_message(author,
                                                    "What is your Sexual Orientation? Please choose from Straight,"
                                                    " Bisexual, Pansexual, Asexual, or Gay.")
                while True:
                    orient = ["straight", "bisexual", "pansexual", "gay", "asexual"]
                    ot = await self.bot.wait_for_message(channel=otmsg.channel, author=author, timeout=60)
                    if ot is None:
                        await self.bot.send_message(author,
                                                    "Registration has timed out. Please run register command again to continue!")
                        break
                    elif ot.content.lower() not in orient:
                        await self.bot.send_message(author,
                                                    "You have entered an incorrect repsonse. Please choose from Straigh"
                                                    "t, Gay, Bisexual, Asexual, or Pansexual. Remember to check your spelling!")
                    elif ot.content.lower() in orient:
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
                                                                  "```Explanation```\n:one:Submissive - This means you "
                                                                  "are passive and not aggressive in relationships\n"
                                                                  ":two:Dominant - This means you are aggressive in "
                                                                  "relationships\n:three:Switch - This means you are "
                                                                  "both passive and aggressive or you 'switch' roles "
                                                                  "in relationships.")
                while True:
                    pos = ["submissive", "dominant", "switch"]
                    position = await self.bot.wait_for_message(channel=positionmsg.channel, author=author, timeout=60)
                    if position is None:
                        await self.bot.send_message(author,
                                                    "Registration has timed out. Please run register command again to continue!")
                        break
                    elif position.content.lower() not in pos:
                        await self.bot.send_message(author,
                                                    "You have entered an incorrect response. Please choose from Submiss"
                                                    "ive, Dominant, or Switch. Remember to check your spelling!")
                    elif position.content.lower() in pos:
                        dom = discord.utils.get(server.roles, name='Dominant')
                        sub = discord.utils.get(server.roles, name='Submissive')
                        switch = discord.utils.get(server.roles, name='Switch')
                        if position.content.lower() == "dominant":
                            await self.bot.add_roles(author, dom)
                            em.add_field(name="Position/Role", value="Dominant", inline=True)
                        elif position.content.lower() == "switch":
                            await self.bot.add_roles(author, switch)
                            em.add_field(name="Position/Role", value="Switch", inline=True)
                        else:
                            await self.bot.add_roles(author, sub)
                            em.add_field(name="Position/Role", value="Submissive", inline=True)
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
                                elif int(age.content) >= 18:
                                    await self.bot.add_roles(author, over18)
                                    em.add_field(name="Age", value=age.content, inline=True)
                                else:
                                    under = discord.utils.get(server.roles, name="Under 18")
                                    em.add_field(name="Age", value=age.content, inline=True)
                                    await self.bot.add_roles(author, under)
                                break
                        except ValueError:
                            await self.bot.send_message(author,
                                                        "Age must be a number. Try again. This field is required!")
                if age is None:
                    break
                locationmsg = await self.bot.send_message(author, 'Please select your location from the following\n'
                                                                  '"usa-eastern", "usa-central", "usa-pacific", "usa-mountain",'
                                                                  '"africa", "asia","australia", "austria", "belgium", "bosnia", "brazil", "bulgaria",'
                                                                  '"canada", "croatia","czech", "denmark", "estonia", "europe", "finland", "france",'
                                                                  '"germany","hungary", "ireland", "israel", "italy", "latvia", "lithuania",'
                                                                  '"macedonia", "mexico", "middle east", "netherlands", "norway",'
                                                                  '"new zealand", "philippines", "poland", "portugal", "romania",'
                                                                  '"russia", "saudi", "scotland", "serbia", "singapore", "slovakia",'
                                                                  '"slovenia", "south america", "spain", "sweden", "switzerland",'
                                                                  '"turkey", "united kingdom"')
                while True:
                    locations = ["usa-eastern", "usa-central", "usa-pacific", "usa-mountain", "africa", "asia",
                                 "australia", "austria", "belgium", "bosnia", "brazil", "bulgaria", "canada", "croatia",
                                 "czech", "denmark", "estonia", "europe", "finland", "france", "germany", "hungary",
                                 "ireland", "israel", "italy", "latvia", "lithuania", "macedonia", "mexico",
                                 "middle-east", "netherlands", "norway", "newzealand", "philippines", "poland",
                                 "portugal", "romania", "russia", "saudi", "scotland", "serbia", "singapore",
                                 "slovakia","slovenia", "southamerica", "spain", "sweden", "switzerland", "turkey",
                                 "unitedkingdom"]
                    location = await self.bot.wait_for_message(channel=locationmsg.channel, author=author, timeout=60)
                    if location is None:
                        await self.bot.send_message(author,
                                                    "Registration has timed out. Please run register command again to continue!")
                        break
                    elif location.content.lower() not in locations:
                        await self.bot.send_message(author,
                                                    "You have chosen an incorrect response. Please select from the list"
                                                    "above")
                    elif location.content.lower() in locations:
                        usa1 = discord.utils.get(server.roles, name="USA-Eastern")
                        usa2 = discord.utils.get(server.roles, name="USA-Central")
                        usa3 = discord.utils.get(server.roles, name="USA-Pacific")
                        usa4 = discord.utils.get(server.roles, name="USA-Mountain")
                        africa = discord.utils.get(server.roles, name="Africa")
                        asia = discord.utils.get(server.roles, name="Asia")
                        australia = discord.utils.get(server.roles, name="Australia")
                        austria = discord.utils.get(server.roles, name="Austria")
                        belgium = discord.utils.get(server.roles, name="Belgium")
                        bosnia = discord.utils.get(server.roles, name="Bosnia")
                        brazil = discord.utils.get(server.roles, name="Brazil")
                        bulgaria = discord.utils.get(server.roles, name="Bulgaria")
                        canada = discord.utils.get(server.roles, name="Canada")
                        croatia = discord.utils.get(server.roles, name="Croatia")
                        czech = discord.utils.get(server.roles, name="Czech")
                        denmark = discord.utils.get(server.roles, name="Denmark")
                        estonia = discord.utils.get(server.roles, name="Estonia")
                        europe = discord.utils.get(server.roles, name="Europe")
                        finland = discord.utils.get(server.roles, name="Finland")
                        france = discord.utils.get(server.roles, name="France")
                        germany = discord.utils.get(server.roles, name="Germany")
                        hungary = discord.utils.get(server.roles, name="Hungary")
                        ireland = discord.utils.get(server.roles, name="Ireland")
                        israel = discord.utils.get(server.roles, name="Israel")
                        italy = discord.utils.get(server.roles, name="Italy")
                        latvia = discord.utils.get(server.roles, name="Latvia")
                        lithuania = discord.utils.get(server.roles, name="Lithuania")
                        macedonia = discord.utils.get(server.roles, name="Macedonia")
                        mexico = discord.utils.get(server.roles, name="Mexico")
                        middleeast = discord.utils.get(server.roles, name="Middle East")
                        netherlands = discord.utils.get(server.roles, name="Netherlands")
                        norway = discord.utils.get(server.roles, name="Norway")
                        newzealand = discord.utils.get(server.roles, name="New Zealand")
                        philippines = discord.utils.get(server.roles, name="Philippines")
                        poland = discord.utils.get(server.roles, name="Poland")
                        portugal = discord.utils.get(server.roles, name="Portugal")
                        romania = discord.utils.get(server.roles, name="Romania")
                        russia = discord.utils.get(server.roles, name="Russia")
                        saudi = discord.utils.get(server.roles, name="Saudi")
                        scotland = discord.utils.get(server.roles, name="Scotland")
                        serbia = discord.utils.get(server.roles, name="Serbia")
                        singapore = discord.utils.get(server.roles, name="Singapore")
                        slovakia = discord.utils.get(server.roles, name="Slovakia")
                        slovenia = discord.utils.get(server.roles, name="Slovenia")
                        southamerica = discord.utils.get(server.roles, name="South America")
                        spain = discord.utils.get(server.roles, name="Spain")
                        sweden = discord.utils.get(server.roles, name="Sweden")
                        switzerland = discord.utils.get(server.roles, name="Switzerland")
                        turkey = discord.utils.get(server.roles, name="Turkey")
                        uk = discord.utils.get(server.roles, name="United Kingdom")
                        em.add_field(name="Location", value=location.content)
                        if location.content.lower() == "usa-eastern":
                            await self.bot.add_roles(author, usa1)
                        elif location.content.lower() == "usa-central":
                            await self.bot.add_roles(author, usa2)
                        elif location.content.lower() == "usa-pacific":
                            await self.bot.add_roles(author, usa3)
                        elif location.content.lower() == "usa-mountain":
                            await self.bot.add_roles(author, usa4)
                        elif location.content.lower() == "africa":
                            await self.bot.add_roles(author, africa)
                        elif location.content.lower() == "asia":
                            await self.bot.add_roles(author, asia)
                        elif location.content.lower() == "australia":
                            await self.bot.add_roles(author, australia)
                        elif location.content.lower() == "austria":
                            await self.bot.add_roles(author, austria)
                        elif location.content.lower() == "belgium":
                            await self.bot.add_roles(author, belgium)
                        elif location.content.lower() == "bosnia":
                            await self.bot.add_roles(author, bosnia)
                        elif location.content.lower() == "brazil":
                            await self.bot.add_roles(author, brazil)
                        elif location.content.lower() == "bulgaria":
                            await self.bot.add_roles(author, bulgaria)
                        elif location.content.lower() == "canada":
                            await self.bot.add_roles(author, canada)
                        elif location.content.lower() == "croatia":
                            await self.bot.add_roles(author, croatia)
                        elif location.content.lower() == "czech":
                            await self.bot.add_roles(author, czech)
                        elif location.content.lower() == "denmark":
                            await self.bot.add_roles(author, denmark)
                        elif location.content.lower() == "estonia":
                            await self.bot.add_roles(author, estonia)
                        elif location.content.lower() == "europe":
                            await self.bot.add_roles(author, europe)
                        elif location.content.lower() == "finland":
                            await self.bot.add_roles(author, finland)
                        elif location.content.lower() == "france":
                            await self.bot.add_roles(author, france)
                        elif location.content.lower() == "germany":
                            await self.bot.add_roles(author, germany)
                        elif location.content.lower() == "hungary":
                            await self.bot.add_roles(author, hungary)
                        elif location.content.lower() == "ireland":
                            await self.bot.add_roles(author, ireland)
                        elif location.content.lower() == "israel":
                            await self.bot.add_roles(author, israel)
                        elif location.content.lower() == "italy":
                            await self.bot.add_roles(author, italy)
                        elif location.content.lower() == "latvia":
                            await self.bot.add_roles(author, latvia)
                        elif location.content.lower() == "lithuania":
                            await self.bot.add_roles(author, lithuania)
                        elif location.content.lower() == "macedonia":
                            await self.bot.add_roles(author, macedonia)
                        elif location.content.lower() == "mexico":
                            await self.bot.add_roles(author, mexico)
                        elif location.content.lower() == "middle east":
                            await self.bot.add_roles(author, middleeast)
                        elif location.content.lower() == "netherlands":
                            await self.bot.add_roles(author, netherlands)
                        elif location.content.lower() == "norway":
                            await self.bot.add_roles(author, norway)
                        elif location.content.lower() == "new zealand":
                            await self.bot.add_roles(author, newzealand)
                        elif location.content.lower() == "philippines":
                            await self.bot.add_roles(author, philippines)
                        elif location.content.lower() == "poland":
                            await self.bot.add_roles(author, poland)
                        elif location.content.lower() == "portugal":
                            await self.bot.add_roles(author, portugal)
                        elif location.content.lower() == "romania":
                            await self.bot.add_roles(author, romania)
                        elif location.content.lower() == "russia":
                            await self.bot.add_roles(author, russia)
                        elif location.content.lower() == "saudi":
                            await self.bot.add_roles(author, saudi)
                        elif location.content.lower() == "scotland":
                            await self.bot.add_roles(author, scotland)
                        elif location.content.lower() == "serbia":
                            await self.bot.add_roles(author, serbia)
                        elif location.content.lower() == "singapore":
                            await self.bot.add_roles(author, singapore)
                        elif location.content.lower() == "slovakia":
                            await self.bot.add_roles(author, slovakia)
                        elif location.content.lower() == "slovenia":
                            await self.bot.add_roles(author, slovenia)
                        elif location.content.lower() == "south america":
                            await self.bot.add_roles(author, southamerica)
                        elif location.content.lower() == "spain":
                            await self.bot.add_roles(author, spain)
                        elif location.content.lower() == "sweden":
                            await self.bot.add_roles(author, sweden)
                        elif location.content.lower() == "switzerland":
                            await self.bot.add_roles(author, switzerland)
                        elif location.content.lower() == "turkey":
                            await self.bot.add_roles(author, turkey)
                        elif location.content.lower() == "united kingdom":
                            await self.bot.add_roles(author, uk)
                        break
                if location is None:
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
