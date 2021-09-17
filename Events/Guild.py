# Imports
import nextcord, pymongo, json, os
from nextcord.ext import commands
from nextcord.ui import View, button
from dotenv import load_dotenv

from Functions.Embed import *
from Views.Dismiss import DismissView

# Get Options.json as Options
with open('Settings/Options.json') as Settings:
    Options = json.load(Settings)

# Get mongodb client object
load_dotenv()
Client = pymongo.MongoClient(f"mongodb+srv://Scrappy:{os.getenv('MongoPassword')}@scrappy.3zhi6.mongodb.net/{Options['Database']['Database']}?retryWrites=true&w=majority")

class GuildProfileManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener('on_guild_join') # Task: Change this back to `on_guild_join` once module complete
    async def GuildJoinListener(self, guild:nextcord.Guild):
        print(guild.text_channels)
        # Get guild profile template
        with open('Settings/Schema/Guild.json', 'r', encoding = 'utf-8') as RawGuildProfile:
            GuildProfileTemplate = json.load(RawGuildProfile)
        
        # Set profile to guild
        GuildProfileTemplate['_id'] = int(guild.id)

        # Insert into database
        Database = Client[Options['Database']['Database']]
        Collection = Database[Options['Database']['Collections']['Guild']]

        try: Collection.insert_one(GuildProfileTemplate)
        except: pass
        
        # Get join message
        with open('Assets/Join.txt', 'r', encoding = 'utf-8') as RawJoinMessage:
            JoinMessage = RawJoinMessage.read()

        # Create Embed
        JoinEmbed = await Custom("Scrappy!", JoinMessage)
    
        # Send embed in the first channel
        channel = guild.text_channels[0]

        view = DismissView()
        view.response = await channel.send(embed = JoinEmbed, view = view)


# Add error handler to the bot
def setup(bot):
    bot.add_cog(GuildProfileManager(bot))