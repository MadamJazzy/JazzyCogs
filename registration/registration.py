import os
import asyncio  # noqa: F401
import discord
import logging
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from cogs.utils import checks


class registration:
    """Custom Cog for Registration and Info Printout"""

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
            await self.bot.say("How to use this cog\n"
                               "1. Run command `setreg channel *channelid*` - This will set the channel for the output"
                               "2. Run command `setreg roles` - This will create the roles needed for the cog to function"
                               "3. Run command `setreg toggle` This will turn on the registration cog")

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

    @checks.admin_or_permissions(Manage_server=True)
    @setreg.command(name="droles", pass_context=True, no_pm=True)
    async def roles2(self, ctx):
        """Deletes roles created when you activated this cog"""
        try:
            setrole = await self.bot.wait_for_message(channel=rolemsg.channel, author=author, timeout=60)
            if setrole.content.lower() == "no":
                await self.bot.reply("OK, This must be done before the command will work correctly!")
            elif setrole.content.lower() == "yes":
                server = ctx.message.server
                author = ctx.message.author
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
                if male in server.roles:
                    await self.bot.delete_role(server, name="Male")
                if female in server.roles:
                    await self.bot.delete_role(server, name="Female")
                if trans in server.roles:
                    await self.bot.delete_role(server, name="Transgender")
                if str8 in server.roles:
                    await self.bot.delete_role(server, name="Straight")
                if gay in server.roles:
                    await self.bot.delete_role(server, name="Gay")
                if bi in server.roles:
                    await self.bot.delete_role(server, name="Bisexual")
                if pan in server.roles:
                    await self.bot.delete_role(server, name="Pansexual")
                if dom in server.roles:
                    await self.bot.delete_role(server, name="Dominant")
                if sub in server.roles:
                    await self.bot.delete_role(server, name="Submissive")
                if switch in server.roles:
                    await self.bot.delete_role(server, name="Switch")
                if over in server.roles:
                    await self.bot.delete_role(server, name="Over 18")
                if reg in server.roles:
                    await self.bot.delete_role(server, name="Registered")
                if under in server.roles:
                    await self.bot.delete_role(server, name="Under 18")
                if mtf in server.roles:
                    await self.bot.delete_role(server, name="Trans MTF")
                if ftm in server.roles:
                    await self.bot.delete_role(server, name="Trans FTM")
                if asexual in server.roles:
                    await self.bot.delete_role(server, name="Asexual")
                if usa1 in server.roles:
                    await self.bot.delete_role(server, name="USA-Eastern")
                if usa2 in server.roles:
                    await self.bot.delete_role(server, name="USA-Central")
                if usa3 in server.roles:
                    await self.bot.delete_role(server, name="USA-Pacific")
                if usa4 in server.roles:
                    await self.bot.delete_role(server, name="USA-Mountain")
                if africa in server.roles:
                    await self.bot.delete_role(server, name="Africa")
                if asia in server.roles:
                    await self.bot.delete_role(server, name="Asia")
                if australia in server.roles:
                    await self.bot.delete_role(server, name="Australia")
                if austria in server.roles:
                    await self.bot.delete_role(server, name="Austria")
                if belgium in server.roles:
                    await self.bot.delete_role(server, name="Belgium")
                if bosnia in server.roles:
                    await self.bot.delete_role(server, name="Bosnia")
                if brazil in server.roles:
                    await self.bot.delete_role(server, name="Brazil")
                if bulgaria in server.roles:
                    await self.bot.delete_role(server, name="Bulgaria")
                if canada in server.roles:
                    await self.bot.delete_role(server, name="Canada")
                if croatia in server.roles:
                    await self.bot.delete_role(server, name="Croatia")
                if czech in server.roles:
                    await self.bot.delete_role(server, name="Czech")
                if denmark in server.roles:
                    await self.bot.delete_role(server, name="Denmark")
                if estonia in server.roles:
                    await self.bot.delete_role(server, name="Estonia")
                if europe in server.roles:
                    await self.bot.delete_role(server, name="Europe")
                if finland in server.roles:
                    await self.bot.delete_role(server, name="Finland")
                if france in server.roles:
                    await self.bot.delete_role(server, name="France")
                if germany in server.roles:
                    await self.bot.delete_role(server, name="Germany")
                if hungary in server.roles:
                    await self.bot.delete_role(server, name="Hungary")
                if ireland in server.roles:
                    await self.bot.delete_role(server, name="Ireland")
                if israel in server.roles:
                    await self.bot.delete_role(server, name="Israel")
                if italy in server.roles:
                    await self.bot.delete_role(server, name="Italy")
                if latvia in server.roles:
                    await self.bot.delete_role(server, name="Latvia")
                if lithuania in server.roles:
                    await self.bot.delete_role(server, name="Lithuania")
                if macedonia in server.roles:
                    await self.bot.delete_role(server, name="Macedonia")
                if mexico in server.roles:
                    await self.bot.delete_role(server, name="Mexico")
                if middleeast in server.roles:
                    await self.bot.delete_role(server, name="Middle East")
                if netherlands in server.roles:
                    await self.bot.delete_role(server, name="Netherlands")
                if norway in server.roles:
                    await self.bot.delete_role(server, name="Norway")
                if newzealand in server.roles:
                    await self.bot.delete_role(server, name="New Zealand")
                if philippines in server.roles:
                    await self.bot.delete_role(server, name="Philippines")
                if poland in server.roles:
                    await self.bot.delete_role(server, name="Poland")
                if portugal in server.roles:
                    await self.bot.delete_role(server, name="Portugal")
                await asyncio.sleep(2.0)
                if romania in server.roles:
                    await self.bot.delete_role(server, name="Romania")
                if russia in server.roles:
                    await self.bot.delete_role(server, name="Russia")
                if saudi in server.roles:
                    await self.bot.delete_role(server, name="Saudi")
                if scotland in server.roles:
                    await self.bot.delete_role(server, name="Scotland")
                if serbia in server.roles:
                    await self.bot.delete_role(server, name="Serbia")
                if singapore in server.roles:
                    await self.bot.delete_role(server, name="Singapore")
                if slovakia in server.roles:
                    await self.bot.delete_role(server, name="Slovakia")
                if slovenia in server.roles:
                    await self.bot.delete_role(server, name="Slovenia")
                if southamerica in server.roles:
                    await self.bot.delete_role(server, name="South America")
                if spain in server.roles:
                    await self.bot.delete_role(server, name="Spain")
                if sweden in server.roles:
                    await self.bot.delete_role(server, name="Sweden")
                if switzerland in server.roles:
                    await self.bot.delete_role(server, name="Switzerland")
                if turkey in server.roles:
                    await self.bot.delete_role(server, name="Turkey")
                if uk in server.roles:
                    await self.bot.delete_role(server, name="United Kingdom")
                await asyncio.sleep(1.0)
                await self.bot.reply("All done!")
            else:
                await self.bot.reply("The command has timed out or you have entered an invalid response. "
                                     "Please only type yes or no. Try again later")
        except discord.HTTPException or discord.Forbidden:
            await self.bot.reply("Removal of roles has failed, The most common problem is that i do not Manage Roles "
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
                    em = discord.Embed(timestamp=ctx.message.timestamp, title="UserID: {}".format(author.id),
                                       color=discord.Color.blue())
                    em.set_author(name='Registration for {}'.format(author.name), icon_url=avatar)
                    em.set_thumbnail(url=avatar)
                    gendermsg = await self.bot.send_message(author, "What is your Gender? Enter only the **Number** \n"
                                                                    "1. Male\n"
                                                                    "2. Female\n"
                                                                    "3. Trans\n"
                                                                    "4. Trans MTF\n"
                                                                    "5. Trans FTM\n"
                                                                    "6. Prefer not to Answer")
                    while True:
                        gender = await self.bot.wait_for_message(channel=gendermsg.channel, author=author, timeout=60)
                        if gender is None:
                            await self.bot.send_message(author,
                                                        "Registration has timed out. Please run register command again to continue!")
                            break
                        male = discord.utils.get(server.roles, name='Male')
                        female = discord.utils.get(server.roles, name='Female')
                        trans = discord.utils.get(server.roles, name='Transgender')
                        mtf = discord.utils.get(server.roles, name="Trans MTF")
                        ftm = discord.utils.get(server.roles, name="Trans FTM")
                        if gender is int:
                            if gender == 1:
                                await self.bot.add_roles(author, male)
                                em.add_field(name="Gender", value="Male", inline=True)
                            elif gender == 2:
                                await self.bot.add_roles(author, female)
                                em.add_field(name="Gender", value="Female", inline=True)
                            elif gender == 4:
                                await self.bot.add_roles(author, mtf)
                                em.add_field(name="Gender", value="Trans MTF", inline=True)
                            elif gender == 5:
                                await self.bot.add_roles(author, ftm)
                                em.add_field(name="Gender", value="Trans FTM", inline=True)
                            elif gender == 3:
                                await self.bot.add_roles(author, trans)
                                em.add_field(name="Gender", value="Transgender", inline=True)
                            elif gender == 6:
                                em.add_field(name="Gender", value="Attack Helicopter")
                        else:
                            self.bot.send_message(author, "You have entered an invalid response. Registration has been canceled.")
                        break
                    if gender is None:
                        break
                except discord.Forbidden:
                    await self.bot.reply("Sorry, You have your DMs disabled. I cannot register you if i cannot DM "
                                         "you. You are more than welcome to disable then again after we are done!")

                otmsg = await self.bot.send_message(author, "What is your Orientation, Please enter only the **Number**\n"
                                                            "1. Straight\n"
                                                            "2. Gay\n"
                                                            "3. Bisexual\n"
                                                            "4. Pansexual\n"
                                                            "5. Asexual\n"
                                                            "6. Prefer not to answer")
                while True:
                    ot = await self.bot.wait_for_message(channel=otmsg.channel, author=author, timeout=60)
                    if ot is int:
                        str8 = discord.utils.get(server.roles, name='Straight')
                        gay = discord.utils.get(server.roles, name='Gay')
                        bi = discord.utils.get(server.roles, name='Bisexual')
                        pan = discord.utils.get(server.roles, name='Pansexual')
                        asexual = discord.utils.get(server.roles, name="Asexual")
                        if ot == 1:
                            await self.bot.add_roles(author, str8)
                            em.add_field(name="Orientation", value="Straight", inline=True)
                        elif ot == 2:
                            await self.bot.add_roles(author, gay)
                            em.add_field(name="Orientation", value="Gay", inline=True)
                        elif ot == 4:
                            await self.bot.add_roles(author, pan)
                            em.add_field(name="Orientation", value="Pansexual", inline=True)
                        elif ot == 5:
                            await self.bot.add_roles(author, asexual)
                            em.add_field(name="Orientation", value="Asexual", inline=True)
                        elif ot == 3:
                            await self.bot.add_roles(author, bi)
                            em.add_field(name="Orientation", value="Bisexual", inline=True)
                        elif ot == 6:
                            em.add_field(name="Orientation", value="Unknown", inline=True)
                        break
                    else:
                        self.bot.send_message(author,
                                              "You have entered an invalid response. Registration has been canceled.")
                        break
                if ot is None:
                    break

                positionmsg = await self.bot.send_message(author,  "Which of the following matches your personality?\n"
                                                                   "1. Submissive - Means you are passive and not aggressive"
                                                                   "2. Dominant - Means you are aggresive and not passive"
                                                                   "3. Switch - Means you are a little of both. "
                                                                   "4. Prefer not to answer")
                while True:
                    position = await self.bot.wait_for_message(channel=positionmsg.channel, author=author, timeout=60)
                    if position is int:
                        dom = discord.utils.get(server.roles, name='Dominant')
                        sub = discord.utils.get(server.roles, name='Submissive')
                        switch = discord.utils.get(server.roles, name='Switch')
                        if position == 2:
                            await self.bot.add_roles(author, dom)
                            em.add_field(name="Position/Role", value="Dominant", inline=True)
                        elif position == 3:
                            await self.bot.add_roles(author, switch)
                            em.add_field(name="Position/Role", value="Switch", inline=True)
                        elif position == 1:
                            await self.bot.add_roles(author, sub)
                            em.add_field(name="Position/Role", value="Submissive", inline=True)
                        elif position == 4:
                            em.add_field(name="Position/Role", value="Undecided", inline=True)
                        break
                    else:
                        self.bot.send_message(author,
                                              "You have entered an invalid response. Registration has been canceled.")
                        break
                if position is None:
                    break
                agemsg = await self.bot.send_message(author, "What is your Age Range?"
                                                             "1. 13-16"
                                                             "2. 16-18"
                                                             "3. 18-22"
                                                             "4. 22-30"
                                                             "5. 30+"
                                                             "6. Prefer Not to Answer")
                while True:
                    over18 = discord.utils.get(server.roles, name="Over 18")
                    under = discord.utils.get(server.roles, name="Under 18")
                    age = await self.bot.wait_for_message(channel=agemsg.channel, author=author, timeout=60)
                    if age is int:
                        if age == 6:
                            em.add_field(name="Age", value="To scared to tell", inline=True)
                        elif age == 3 or 4 or 5:
                            await self.bot.add_roles(author, over18)
                            em.add_field(name="Age", value=age.content, inline=True)
                        elif age == 1 or 2:
                            em.add_field(name="Age", value=age.content, inline=True)
                            await self.bot.add_roles(author, under)
                    else:
                        self.bot.send_message(author,
                                              "You have entered an invalid response. Registration has been canceled.")
                        break
                if age is None:
                    break
                locationmsg = await self.bot.send_message(author, "Please select your location from the following. Enter only the **NUMBER**\n"
                                                                  "*This is for ROLE only. It will not be displayed on your Profile*"
                                                                  " 1. USA-Eastern    2. USA-Central    3. USA-Pacific\n"
                                                                  " 4. USA-Mountain   5. Africa         6. Asia\n"
                                                                  " 7. Australia      8. Belgium        9. Bosnia\n"
                                                                  "10. Brazil        11. Bulgaria      12. Canada\n"
                                                                  "13. Croatia       14. Czech         15. Denmark\n"
                                                                  "16. Estonia       17. Europe        18. Finland\n"
                                                                  "19. France        20. Germany       21. Hungary\n"
                                                                  "22. Ireland       23. Israel        24. Italy\n"
                                                                  "25. Latvia        26. Lithuania     27. Macedonia\n"
                                                                  "28. Mexico        29. Middle East   30. Netherlands\n"
                                                                  "31. Norway        32. New Zealand   33. Philippines\n"
                                                                  "34. Poland        35. Portugal      36. Romania\n"
                                                                  "37. Russia        38. Saudi         39. Scotland\n"
                                                                  "40. Serbia        41. Singapore     42. Slovakia\n"
                                                                  "43. Solvenia      44. South America 45. Spain\n"
                                                                  "46. Sweden        47. Switzerland   48. Turkey\n"
                                                                  "49. U Kingdom     50. Austria\n"
                                                                  " 0. **NONE**")
                while True:
                    location = await self.bot.wait_for_message(channel=locationmsg.channel, author=author, timeout=60)
                    if location is int:
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
                        if location == 1:
                            await self.bot.add_roles(author, usa1)
                        elif location == 2:
                            await self.bot.add_roles(author, usa2)
                        elif location == 3:
                            await self.bot.add_roles(author, usa3)
                        elif location == 4:
                            await self.bot.add_roles(author, usa4)
                        elif location == 5:
                            await self.bot.add_roles(author, africa)
                        elif location == 6:
                            await self.bot.add_roles(author, asia)
                        elif location == 7:
                            await self.bot.add_roles(author, australia)
                        elif location == 50:
                            await self.bot.add_roles(author, austria)
                        elif location == 8:
                            await self.bot.add_roles(author, belgium)
                        elif location == 9:
                            await self.bot.add_roles(author, bosnia)
                        elif location == 10:
                            await self.bot.add_roles(author, brazil)
                        elif location == 11:
                            await self.bot.add_roles(author, bulgaria)
                        elif location == 12:
                            await self.bot.add_roles(author, canada)
                        elif location == 13:
                            await self.bot.add_roles(author, croatia)
                        elif location == 14:
                            await self.bot.add_roles(author, czech)
                        elif location == 15:
                            await self.bot.add_roles(author, denmark)
                        elif location == 16:
                            await self.bot.add_roles(author, estonia)
                        elif location == 17:
                            await self.bot.add_roles(author, europe)
                        elif location == 18:
                            await self.bot.add_roles(author, finland)
                        elif location == 19:
                            await self.bot.add_roles(author, france)
                        elif location == 20:
                            await self.bot.add_roles(author, germany)
                        elif location == 21:
                            await self.bot.add_roles(author, hungary)
                        elif location == 22:
                            await self.bot.add_roles(author, ireland)
                        elif location == 23:
                            await self.bot.add_roles(author, israel)
                        elif location == 24:
                            await self.bot.add_roles(author, italy)
                        elif location == 25:
                            await self.bot.add_roles(author, latvia)
                        elif location == 26:
                            await self.bot.add_roles(author, lithuania)
                        elif location == 27:
                            await self.bot.add_roles(author, macedonia)
                        elif location == 28:
                            await self.bot.add_roles(author, mexico)
                        elif location == 29:
                            await self.bot.add_roles(author, middleeast)
                        elif location == 30:
                            await self.bot.add_roles(author, netherlands)
                        elif location == 31:
                            await self.bot.add_roles(author, norway)
                        elif location == 32:
                            await self.bot.add_roles(author, newzealand)
                        elif location == 33:
                            await self.bot.add_roles(author, philippines)
                        elif location == 34:
                            await self.bot.add_roles(author, poland)
                        elif location == 35:
                            await self.bot.add_roles(author, portugal)
                        elif location == 36:
                            await self.bot.add_roles(author, romania)
                        elif location == 37:
                            await self.bot.add_roles(author, russia)
                        elif location == 38:
                            await self.bot.add_roles(author, saudi)
                        elif location == 39:
                            await self.bot.add_roles(author, scotland)
                        elif location == 40:
                            await self.bot.add_roles(author, serbia)
                        elif location == 41:
                            await self.bot.add_roles(author, singapore)
                        elif location == 42:
                            await self.bot.add_roles(author, slovakia)
                        elif location == 43:
                            await self.bot.add_roles(author, slovenia)
                        elif location == 44:
                            await self.bot.add_roles(author, southamerica)
                        elif location == 45:
                            await self.bot.add_roles(author, spain)
                        elif location == 46:
                            await self.bot.add_roles(author, sweden)
                        elif location == 47:
                            await self.bot.add_roles(author, switzerland)
                        elif location == 48:
                            await self.bot.add_roles(author, turkey)
                        elif location == 49:
                            await self.bot.add_roles(author, uk)
                        elif location == 0:
                            pass
                    else:
                        self.bot.send_message(author,
                                              "You have entered an invalid response. Registration has been canceled.")
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
