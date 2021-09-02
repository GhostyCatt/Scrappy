import nextcord, pymongo, json, os
from nextcord.ext import commands
from nextcord.ui import View, button
from dotenv import load_dotenv

from Functions.Embed import *

# Get Options.json as Options
with open('Settings/Options.json') as Settings:
    Options = json.load(Settings)

# Load .Env file 
load_dotenv()

# Get mongodb client object
Client = pymongo.MongoClient(f"mongodb+srv://Scrappy:{os.getenv('MongoPassword')}@scrappy.3zhi6.mongodb.net/{Options['Database']['Database']}?retryWrites=true&w=majority")



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


    @commands.Cog.listener('on_guild_join') # Task: Change this back to `on_guild_join` once module complete
    async def GuildJoinListener(self, guild:nextcord.Guild):
        """
        Guild Join Listener
        ------------

        Triggers when bot joins a guild.
        """
        # Get guild profile template
        with open('Settings/Schema/Guild.json', 'r', encoding = 'utf-8') as RawGuildProfile:
            GuildProfileTemplate = json.load(RawGuildProfile)
        
        # Set profile to guild
        GuildProfileTemplate['_id'] = int(guild.id)

        # Insert into database
        Database = Client[Options['Database']['Database']]
        Collection = Database[Options['Database']['Collections']['Guild']]

        try:
            Collection.insert_one(GuildProfileTemplate)
        except:
            pass
        
        # Create Embed
        JoinEmbed = await Custom(
            Options['Emojis']['Integration'],
            "Scrappy!",
            "Hey there!\n\nThanks for adding me to your server :D\nMy prefix, by default, is `.`"
        )
        
        try:
            # Get # General
            general = nextcord.utils.find(lambda x: x.name == 'general',  guild.text_channels)

            if general and general.permissions_for(guild.me).send_messages:
                # Send the embed in #general if possible
                view = ButtonArray()
                await general.send(embed = JoinEmbed, view = view)

        except: pass


# Add error handler to the bot
def setup(bot):
    bot.add_cog(GuildProfileManager(bot))