import nextcord, json
from nextcord.ext import commands

from Functions.Embed import *
from Views.Help import HelpView
from Views.Dismiss import DismissView

# Load Options.json as a dict
with open('Settings/Options.json') as Settings:
    Options = json.load(Settings)

# Ignore these cogs in the help command
cog_ignore = ["CommandErrorHandler", "GuildProfileManager", "Isolated Commands"]

class Help(commands.HelpCommand):
    def get_command_signature(self, command):
        # Create clean string with prefix, name and signature
        return '%s%s %s' % (Options['Prefix'], command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        # Create Embed
        embed = await Normal(f"A role management discord bot.\n\nThis is a list of all the modules in the bot. Use the command `{Options['Prefix']}help <command>` or `{Options['Prefix']}help <module>` for more.")
        embed.set_author(name = "Scrappy")

        # Add a new field for every cog in the bot
        for cog, commands in mapping.items():
            name = getattr(cog, "qualified_name", "Isolated Commands")

            if name in cog_ignore: pass
            else:
                embed.add_field(name = f"**{name}**", value = f"> `{Options['Prefix']}help {name}`", inline = True)
        
        # Send embed with button interactions
        view = HelpView(self.context)
        view.response = await self.context.send(embed = embed, view = view)

    async def send_cog_help(self, cog):
        # Get module name / description
        name = getattr(cog, "qualified_name", "No Category")
        description = getattr(cog, "description", "No description provided")

        # Create Embed
        embed = await Normal(f"{description}\n\nUse the command `{Options['Prefix']}help <command>` or `{Options['Prefix']}help <module>` for more.")
        embed.set_author(name = "Scrappy")

        # Add a new field for each command in the module
        for command in cog.walk_commands():
            if command.parent != None:
                pass
            else:
                name = getattr(command, "name", "CommandName")
                description = getattr(command, "help", "No description provided")

                embed.add_field(name = f"**{name}**", value = f"> {command.help}", inline = False)
        
        # Send embed with button interactions
        view = HelpView(self.context)
        view.response = await self.context.send(embed = embed, view = view)

    async def send_command_help(self, command):
        # Get command info
        name = getattr(command, "name", "Unnamed")
        description = getattr(command, "help", "No description provided")
        usage = getattr(command, "signature", "")
        aliases = getattr(command, "aliases", "None")

        # Create Embed
        embed = await Normal(f"**{description}**\n\n**Usage** » `{Options['Prefix']}{name.lower()} {usage}`\n**Aliases** » `{aliases}`")
        embed.set_author(name = name.capitalize())
         
        # Send embed with button interactions
        view = HelpView(self.context)
        view.response = await self.context.send(embed = embed, view = view)

    async def send_group_help(self, group):
        # Get command info
        name = getattr(group, "name", "No name provided")
        description = getattr(group, "help", "No description provided")

        # Create Embed
        embed = await Normal(f"**{description}**")
        embed.set_author(name = name.capitalize())

        # Add a field for every subcommand
        for command in group.commands:
            command = group.get_command(command.name)

            # Get subcommand info
            name = getattr(command, "name", "Unnamed")
            description = getattr(command, "help", "No description provided")
            usage = getattr(command, "signature", "")
            aliases = getattr(command, "aliases", "None")

            # Add field
            embed.add_field(name = name, value = f"{description}\n**Usage** » `{Options['Prefix']}{name.lower()} {usage}`\n**Aliases** » {aliases}", inline = False)
        
        # Send embed with button interactions
        view = HelpView(self.context)
        view.response = await self.context.send(embed = embed, view = view)

    async def send_error_message(self, error):
        """Send error message in help command"""
        channel = self.get_destination()

        # Create Embed
        embed = await Fail(f"{error}")

        # Send embed with button interactions
        view = DismissView()
        view.response = await channel.send(embed = embed, view = view)