import discord 
from discord.ext import commands
from discord import app_commands

# irrelevant stuff
import datetime
import boto3
import pandas as pd

# secret token
BUCKET_NAME_RESULT = 'job-description-process'

class CheckJobScrapingStatus(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    # get the result from scrapers
    async def GetResultFromS3(self):
        result = {}

        # boto client
        s3 = boto3.client('s3')
        # list all directories
        response = s3.list_objects_v2(Bucket=BUCKET_NAME_RESULT, Delimiter='/')
        print('all scrapers: ', response)


        # Go to each folder and go to the folder with the following name: result-2021-08-01 (replace with current date)
        # get the result from the folder
        for prefix in response.get('CommonPrefixes', []):
            dir_name = prefix.get('Prefix')
            scraper_name = dir_name.split('/')[0]

            print('dir_name: ', dir_name)

            # Check if the directory matches the desired name format
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # the folder name
            folder_name = 'result-'+current_date+'/'
            print('folder_name: ', folder_name)

            # list object inside the folder
            response = s3.list_objects_v2(Bucket=BUCKET_NAME_RESULT, Prefix=f'{dir_name}{folder_name}')

            # get all the files inside that folder
            file_name_list = []
            for obj in response.get('Contents', []):
                # if it is csv file, then proceed
                if obj.get('Key').endswith('.csv'):

                    file_key = obj.get('Key')

                    # read the file with pandas
                    df = pd.read_csv(f's3://{BUCKET_NAME_RESULT}/{file_key}')

                    # get the number of row
                    num_row = df.shape[0]
                    # get the file name
                    file_name = file_key.split('/')[-1]

                    # remove the .csv from the file name
                    file_name = file_name.replace('.csv', f': **{num_row} jobs**')
                    # key of dict is the scraper name, value is the file name
                    file_name_list.append(file_name)
                    # now add the scraper name and file name to the result dict
                    result[scraper_name] = file_name_list

        return result

    @app_commands.command(name='check-job-scraping-status', description='Check the status of the job scraping')
    async def check_job_scraping_status(self, interaction: discord.Interaction):

        try:
            # wait while scrap data
            await interaction.response.defer(thinking=True)

            # get the result from scrapers
            result = await self.GetResultFromS3()

            # if the result is empty dict, then no result
            if not result:
                await interaction.followup.send("No result yet")
            else:
                # if there is result, then send the result
                result_embed = discord.Embed(title="Job Scraping Result", color=0x00ff00)

                # add fields to the embed
                for scraper_name, file_name_list in result.items():
                    # read the file in file_name_list

                    # add the scraper name
                    result_embed.add_field(name=scraper_name, value='\n'.join(file_name_list), inline=False)

                await interaction.followup.send(embed=result_embed)

        except Exception as e:
            await interaction.followup.send(f"Error: {e}")

async def setup(client: commands.Bot):
    await client.add_cog(CheckJobScrapingStatus(client))


