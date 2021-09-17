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
    def __init__(self, ctx):
        super().__init__(timeout = 30)

        self.response = None
        self.ctx = ctx
        
        self.add_item(nextcord.ui.Button(label = "Invite Me", url = Options['InviteLink']))
        self.add_item(nextcord.ui.Button(label = "Website", url = Options['Website']))
    

    @button(label = 'Home Page', style = nextcord.ButtonStyle.green)
    async def dash_home(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """Return to home page"""
        await interaction.response.edit_message(embed = self.homepage)


    @button(label = 'Disable', style = nextcord.ButtonStyle.red)
    async def  dash_cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """Disable all interactions"""
        for child in self.children:
            child.disabled = True  
        await self.response.edit(view = self)
        
        self.stop()


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