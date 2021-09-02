import nextcord, pymongo, json
from nextcord.ext import commands
from nextcord.ui import View, button

from Functions.Embed import *


class ButtonArray(View):
    """
    ButtonArray
    -----------
    
    Contents: 
    
    * Dismiss Button: Deletes Interaction Message

    Arguments: 

    * Context
    """
    def __init__(self, ctx):
        super().__init__(timeout = 30)

        self.response = None
        self.ctx = ctx
    

    @button(label = '⛔ Dismiss', style = nextcord.ButtonStyle.blurple)
    async def  dash_cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()
    

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True  
            
        await self.response.edit(view = self)

class GuildProfileManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener('on_message') # Task: Change this back to `on_guild_join` once module complete
    async def GuildJoinListener(self, guild:nextcord.Guild):
        """
        Guild Join Listener
        ------------

        Triggers when bot joins a guild.
        """
        with open('Settings/Schema/Guild.json', 'r', encoding = 'utf-8') as RawGuildProfile:
            GuildProfileTemplate = json.load(RawGuildProfile)
        
        print(GuildProfileTemplate)


# Add error handler to the bot
def setup(bot):
    bot.add_cog(GuildProfileManager(bot))