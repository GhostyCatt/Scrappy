# Imports
import nextcord
from nextcord.ext import commands

# Functions
async def Success(text:str, ctx:commands.Context = None, timeout:int = None):
    embed = nextcord.Embed(description = f"`✔️` {text}", color = nextcord.Colour.green())

    if not ctx:
        return embed
    else:
        if timeout != None:
            message = await ctx.reply(embed = embed, mention_author = False, delete_after = timeout)
            return message
        else:
            message = await ctx.reply(embed = embed, mention_author = False)
            return message

async def Normal(text:str, ctx:commands.Context = None, timeout:int = None):
    embed = nextcord.Embed(description = f"`🔘` {text}", color = nextcord.Colour.light_grey())

    if not ctx:
        return embed
    else:
        if timeout != None:
            message = await ctx.reply(embed = embed, mention_author = False, delete_after = timeout)
            return message
        else:
            message = await ctx.reply(embed = embed, mention_author = False)
            return message

async def Fail(text:str, ctx:commands.Context = None, timeout:int = None):
    embed = nextcord.Embed(description = f"`❌` {text}", color = nextcord.Colour.red())

    if not ctx:
        return embed
    else:
        if timeout != None:
            message = await ctx.reply(embed = embed, mention_author = False, delete_after = timeout)
            return message
        else:
            message = await ctx.reply(embed = embed, mention_author = False)
            return message