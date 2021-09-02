import nextcord, json, os, sys
from nextcord.ext import commands
from nextcord.ui import View, button

from Functions.Embed import *


# Get Settings.json
with open("Settings/Options.json", "r") as Settings:
    Options = json.load(Settings)
    
# Buttons array for developer commands
class ButtonArray(View):
    def __init__(self, ctx):
        super().__init__(timeout = 30)

        self.response = None
        self.ctx = ctx
    

    @nextcord.ui.button(label = 'Confirm', style = nextcord.ButtonStyle.green)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """Confirm action"""
        if interaction.user.id == self.ctx.author.id:
            for child in self.children:
                child.disabled = True  
            await self.response.edit(view = self)
            
            self.stop()
            self.value = True
        else:
            await interaction.response.send_message("You don't have the permission to use that button!", ephemeral = True)


    @nextcord.ui.button(label = 'Cancel', style = nextcord.ButtonStyle.red)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """Cancel action"""
        if interaction.user.id == self.ctx.author.id:
            for child in self.children:
                child.disabled = True  
            await self.response.edit(view = self)
            
            self.stop()
            self.value = False
        else:
            await interaction.response.send_message("You don't have the permission to use that button!", ephemeral = True)
    

    async def on_timeout(self):
        """Disable all buttons on timeout"""
        for child in self.children:
            child.disabled = True  
            
        await self.response.edit(view = self)

class Developer(commands.Cog):
    """Developer only commands. These are meant to control the bot."""
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    

    def cog_check(self, ctx: commands.Bot):
        return ctx.author.id in Options["Developers"]
    

    @commands.command(name = "Reload", aliases = ["rl"])
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  reload(self, ctx: commands.Context, cog: str):
        """Reload a cog."""
        await ctx.channel.trigger_typing()

        view = ButtonArray(ctx)
        embed = await Custom("", "Confirm", f"Are you sure you want to reload `{cog}`?")
        view.response = await ctx.send(embed = embed, view = view)

        try:
            await view.wait()

            if view.value:
                cogs = self.bot.extensions

                if cog in cogs:
                    self.bot.unload_extension(cog)
                    self.bot.load_extension(cog)
                    embed = await Success(f"**`{cog}`** Has been reloaded")
                    await view.response.edit(embed = embed)

                else:
                    embed = await Fail(f"**`{cog}`** Doesn't exist.")
                    await view.response.edit(embed = embed)
            else:pass
        except:pass


    @commands.command(name = "ListCogs", aliases = ["lc"])
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  listcogs(self, ctx: commands.Context):
        """Get a list of active cogs."""
        await ctx.channel.trigger_typing()

        base_string = "```css\n"
        base_string += "\n- - - - - - - - - - - - - - - - -\n"
        base_string += "\n".join([str(cog) for cog in self.bot.extensions])
        base_string += "\n- - - - - - - - - - - - - - - - -```"
        
        embed = await Custom("Cogs List", base_string)
        await ctx.reply(embed = embed)


    @commands.command(name = "Load")
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  load(self, ctx: commands.Context, cog: str):
        """Load an unloaded cog."""
        await ctx.channel.trigger_typing()

        view = ButtonArray(ctx)
        embed = await Custom("", "Confirm", f"Are you sure you want to load `{cog}`?")
        view.response = await ctx.send(embed = embed, view = view)

        try:
            await view.wait()

            if view.value:
                try:
                    self.bot.load_extension(cog)
                    embed = await Success(f"**`{cog}`** Has been reloaded.")
                    await view.response.edit(embed = embed)

                except commands.errors.ExtensionNotFound:
                    embed = await Fail(f"**`{cog}`** Doesn't exist")
                    await view.response.edit(embed = embed)

                except commands.errors.ExtensionAlreadyLoaded:
                    embed = await Fail(f"**`{cog}`** Was already loaded")
                    await view.response.edit(embed = embed)
            else:pass
        except:pass


    @commands.command(name = "Unload", aliases = ["ul"])
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  unload(self, ctx: commands.Context, cog: str):
        """Unloads a loaded cog."""
        await ctx.channel.trigger_typing()

        view = ButtonArray(ctx)
        embed = await Custom("", "Confirm", f"Are you sure you want to unload `{cog}`?")
        view.response = await ctx.send(embed = embed, view = view)

        try:
            await view.wait()

            if view.value:
                try:
                    self.bot.unload_extension(cog)
                    embed = await Success(f"**`{cog}`** Has been reloaded.")
                    await view.response.edit(embed = embed)

                except commands.errors.ExtensionNotFound:
                    embed = await Fail(f"**`{cog}`** Doesn't exist")
                    await view.response.edit(embed = embed)

                except commands.errors.ExtensionNotLoaded:
                    embed = await Fail(f"**`{cog}`** Was already unloaded")
                    await view.response.edit(embed = embed)
            else:pass
        except:pass
    

    @commands.command(name = "Shutdown")
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  shutdown(self, ctx: commands.Context):
        """Shuts the entire bots code down."""
        await ctx.channel.trigger_typing()

        view = ButtonArray(ctx)
        embed = await Custom("", "Confirm", f"Are you sure you want to shutdown?")
        view.response = await ctx.send(embed = embed, view = view)

        try:
            await view.wait()

            if view.value:
                embed = await Success(f"Bot is shutting down.")
                await view.response.edit(embed = embed)

                await self.bot.close()
            else:pass           
        except:pass


    @commands.command(name = "Restart")
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  restart(self, ctx: commands.Context):
        """Restarts the entire bot code."""
        await ctx.channel.trigger_typing()

        view = ButtonArray(ctx)
        embed = await Custom("", "Confirm", f"Are you sure you want to restart?")
        view.response = await ctx.send(embed = embed, view = view)

        try:
            await view.wait()

            if view.value:
                embed = await Success(f"Bot is restarting. Please wait a few seconds!")
                await view.response.edit(embed = embed)
                
                os.execv(sys.executable, ["python"] + sys.argv)
            else:
                pass
        except:pass
    

# Add developer cog to the bot
def setup(bot:commands.Bot):
    bot.add_cog(Developer(bot))