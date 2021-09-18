# Imports
import nextcord, json
from nextcord.ext import commands
from nextcord.ui import View, Select, button

from Functions.Embed import *

# Load Options.json as a dict
with open('Settings/Options.json') as Settings:
    Options = json.load(Settings)


# Button array for the main help command embed
class HelpView(View):
    def __init__(self, ctx:commands.Context):
        super().__init__(timeout = 30)

        self.ctx = ctx

        self.add_item(nextcord.ui.Button(label = "Invite Me", url = Options['InviteLink']))
        self.add_item(nextcord.ui.Button(label = "Website", url = Options['Website']))

    @button(label = '🗑️', style = nextcord.ButtonStyle.red)
    async def  delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """Delete the interaction"""
        await interaction.message.delete()
        await self.ctx.message.delete()

    async def on_timeout(self):
        """Disable all interactions on timeout"""
        try:
            for child in self.children:
                child.disabled = True  
            await self.response.edit(view = self)
        except: pass
    

    async def interaction_check(self, interaction: nextcord.Interaction):
        """Make it so that only the author can use the interactions"""
        return interaction.user.id == self.ctx.author.id