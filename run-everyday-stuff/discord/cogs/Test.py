import discord 
from discord.ext import commands
from discord import app_commands
from discord.ui import Select, View

from discord import ui
import numpy as np

class Test(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name='testselection', description='This will send you the selection')
    async def testselection(self, interaction: discord.Interaction):
        select = Select(options=[
            discord.SelectOption(label='Red', description='Your favourite color is red', emoji='🟥'),
            discord.SelectOption(label='Green', description='Your favourite color is green', emoji='🟩'),
            discord.SelectOption(label='Blue', description='Your favourite color is blue', emoji='🟦')
            
            ])
        
        # fun part

        async def my_callback(interaction: discord.Interaction):
            await interaction.response.send_message(f'You chose {interaction.data["values"][0]}', ephemeral=True)

        select.callback = my_callback

        view = View()
        view.add_item(select)     

        await interaction.response.send_message('Choose your favourite color:', view=view)   



async def setup(client: commands.Bot):
    await client.add_cog(Test(client))