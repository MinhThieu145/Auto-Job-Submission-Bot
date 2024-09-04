import discord 
from discord.ext import commands
from discord import app_commands

from discord import ui
import numpy as np

import GetJobApplicationData

class SelectToView(commands.Cog):

    # the scraper selected
    scraper_selected = ''

    def __init__(self, client: commands.Bot):
        self.client = client

    # get the result from scrapers
    scraper_result = GetJobApplicationData.GetDataAndDataframe()
    print('scraper_result: ', scraper_result)

    # first get the list of scraper name
    scraper_name_list = scraper_result.keys()
    print('scraper_name_list: ', scraper_name_list)

    # create choices for the scraper_name_list
    scraper_choices = []
    for scraper_name in scraper_name_list:
        scraper_choices.append(app_commands.Choice(name=scraper_name, value=scraper_name))

    @app_commands.command(name='choosescraper', description='Choose a scraper')
    @app_commands.describe(scraper_choices='The scraper you want to choose')
    @app_commands.choices(scraper_choices=scraper_choices)
    async def choosecolor(self, interaction: discord.Interaction, scraper_choices: app_commands.Choice[str]):
        # defer
        await interaction.response.defer()

        global scraper_selected
        scraper_selected = scraper_choices.value

        # okay, now we get the list of file name
        scraper_result = GetJobApplicationData.GetDataAndDataframe()
        file_name_list = scraper_result.get(scraper_selected)

        # create choices for the file_name_list
        file_choices = []
        for file_name in file_name_list:
            file_choices.append(discord.SelectOption(label=file_name))

        # create the select
        if file_choices != []:
            select = discord.ui.Select(options=file_choices)

            # fun part
            async def my_callback(interaction: discord.Interaction):

                # get the dataframe
                df = scraper_result.get(scraper_selected).get(interaction.data["values"][0])

                # loop through each row in the dataframe
                for index, row in df.iterrows():

                    # now prepare the embed for the file
                    embed = discord.Embed(title=row.loc['job_title'], description=row.loc['job_summary'], color=discord.Color.dark_purple(), url=row.loc['job_link'])
                    embed.set_author(name=f'{scraper_selected}')

                    # add a field called technical skills. This is a list of skills
                    key_details = row.loc['key_details']

                    key_details = eval(key_details)
                    # convert the Series technical_skills to a list
                    technical_skills = key_details.get('Technical Skills')

                    # if the technical skills is not empty
                    if technical_skills != []:
                        # convert it to a nice markdown list
                        technical_skills = '\n'.join([f'- {skill}' for skill in technical_skills])

                        # add a field called technical skills
                        embed.add_field(name='Technical Skills', value=technical_skills, inline=False)

                    # send directly the embed
                    await interaction.channel.send(embed=embed)

       

                await interaction.response.send_message(f'You chose {interaction.data["values"][0]}', ephemeral=True, embed=embed)

            select.callback = my_callback

            view = ui.View()
            view.add_item(select)

            await interaction.followup.send('Your selected file:', view=view)

        else:
            await interaction.followup.send('The scraper result is empty.')
                
        
async def setup(client: commands.Bot):
    await client.add_cog(SelectToView(client))