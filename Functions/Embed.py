import nextcord, json

# Get configuration.json
with open("Settings/Options.json", "r") as Settings:
    Options = json.load(Settings)

async def Success(description):
    """
    Success
    -------
    
    Inputs
    * Description: `String`
    """
    embed = nextcord.Embed(
        title = f"Done!",
        description = description,
        color = int(Options["Colors"]["Success"], 16)
    )
    return embed


async def Fail(description):
    """
    Fail
    ----
    
    Inputs
    * Description: `String`"""
    embed = nextcord.Embed(
        title = f"Something went wrong!",
        description = description,
        color = int(Options["Colors"]["Fail"], 16)
    )
    return embed


async def Custom(icon, title, description):
    """
    Custom
    ------
    
    Inputs
    * Icon: `Emoji String`
    * Title: `Short String`
    * Description: `String`
    """
    embed = nextcord.Embed(
        title = f"{icon} {title}!",
        description = description,
        color = int(Options["Colors"]["Neutral"], 16)
    )
    return embed