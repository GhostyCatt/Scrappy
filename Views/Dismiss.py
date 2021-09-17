# Imports
import nextcord
from nextcord.ui import View, button

# Dismiss Class
class DismissView(View):
    def __init__(self):
        super().__init__(timeout = 60)

    @button(label = '⛔ Dismiss', style = nextcord.ButtonStyle.blurple)
    async def  dash_cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True  
            
        await self.response.edit(view = self)