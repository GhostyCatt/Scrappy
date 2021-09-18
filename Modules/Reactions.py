# Imports
import nextcord, pymongo, json, os
from nextcord.ext import commands
from dotenv import load_dotenv

from Functions.Embed import *

# Get Options.json as Options
with open('Settings/Options.json') as Settings:
    Options = json.load(Settings)

# Get mongodb client object
load_dotenv()
Client = pymongo.MongoClient(f"mongodb+srv://Scrappy:{os.getenv('MongoPassword')}@scrappy.3zhi6.mongodb.net/{Options['Database']['Database']}?retryWrites=true&w=majority")

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_raw_reaction_add')
    async def ReactionListener(self, payload:nextcord.RawReactionActionEvent):
        # Get guild profile from database
        Database = Client[Options['Database']['Database']]
        Collection = Database[Options['Database']['Collections']['Guild']]

        GuildProfile = Collection.find_one({"_id": int(payload.guild_id)})

        # End process after a few checks
        if not GuildProfile: return
        if GuildProfile['Reactionrole']['Message'] == None or GuildProfile['Reactionrole']['Status'] == False: return
        if payload.message_id != GuildProfile['Reactionrole']['Message']: return

        for Entry in GuildProfile['Reactionrole']['Options']:
            if Entry['Display'] == None:
                pass
            else:
                if payload.emoji



# Add error handler to the bot
def setup(bot):
    bot.add_cog(ReactionRoles(bot))