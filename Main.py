import nextcord, os, json
from nextcord.ext import commands
from dotenv import load_dotenv
from colorama import init, Fore 

from Modules.HelpCommand import Help

# Load Options.json as a dict
with open('Settings/Options.json') as Settings:
    Options = json.load(Settings)

# Initialise Bot object
intents = nextcord.Intents.all()
intents.members = True
intents.guilds = True

Bot = commands.Bot(
    command_prefix = Options['Prefix'],
    case_insensitive = True,
    help_command = Help(),
    status = nextcord.Status.idle,
    intents = intents
)

# Initialise Colorama for console messages
init(autoreset = True)

# Alert console when bot connects to discord
@Bot.event
async def on_ready():
    print(
        Fore.LIGHTRED_EX + "Logged into Discord\n" +
        Fore.RED + f"Nextcord Version: {nextcord.__version__}\n" +
        Fore.RED + f"Scrappy Version: v4"
    )

# Load all cogs
cogs = [
    # Commands

    # Events
    "Events.Guild",

    # Modules
    "Modules.ErrorHandler",
    "Modules.Reactions",
]

if __name__ == '__main__':
    for extension in cogs:
        try:
            Bot.load_extension(extension)
        except Exception as error:
            print(error)

# Run the bot
load_dotenv()
Bot.run(os.getenv("DiscordToken"))