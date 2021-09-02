import nextcord, pymongo, os, json
from nextcord.ext import commands
from dotenv import load_dotenv

# Get Options.json as Options
with open('Settings/Options.json') as Settings:
    Options = json.load(Settings)

# Load .Env file 
load_dotenv()

# Get mongodb client object
Client = pymongo.MongoClient(f"mongodb+srv://Scrappy:{os.getenv('MongoPassword')}@scrappy.3zhi6.mongodb.net/{Options['Database']['Database']}?retryWrites=true&w=majority")


def GetPrefix(Bot: commands.Bot, Message: nextcord.Message):
    """
    GetPrefix
    ---------
    Get the guild prefix from the database

    * Returns:  `string` value
    * Inputs: `Bot: commands.Bot`, `Message: nextcord.Message`
    """
    # Connect to Database
    Database = Client[Options['Database']['Database']]
    Collection = Database[Options['Database']['Collections']['Guild']]

    # Get guild from database
    GuildData = Collection.find_one(
        {"_id": int(Message.guild.id)}
    )

    try:
        # Get and return prefix
        Prefix = GuildData['Options']['Prefix']
    except:
        Prefix = "."
    return Prefix