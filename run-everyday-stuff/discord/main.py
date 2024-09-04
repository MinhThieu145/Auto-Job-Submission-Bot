import discord
import asyncio
from discord import app_commands
from discord.ext import commands
import requests

# non related stuff
import datetime
import os

# import GetJobApplicationData.py
import sys
sys.path.append('./ExtraFunction') 


# secret token
BOT_TOKEN = ''
CHANNEL_ID = 1121600062263410790

# bot client
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# innitialize the bot
class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix= commands.when_mentioned ,intents= discord.Intents.default())
        self.cog_list = ['cogs.CheckJobScrapingStatus', 'cogs.SelectToView', 'cogs.Test']

    async def setup_hook(self):
        for ext in self.cog_list:
            await self.load_extension(ext)

    async def on_ready(self):
        synced = await self.tree.sync()

        # get the len of the tree
        num_sync_command = len(synced)
        # get the current dir
        current_dir = os.getcwd()
        # find the path to a folder called cogs
        cogs_dir = os.path.join(current_dir, 'cogs')

        # get all the python files in the cogs folder
        cogs_files = [f for f in os.listdir(cogs_dir) if os.path.isfile(os.path.join(cogs_dir, f)) and f.endswith('.py')]
        
        print(num_sync_command)
        if num_sync_command == len(cogs_files) :
            # send message to the channel
            channel = self.get_channel(CHANNEL_ID)

            # get current date and time under the nice format
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # send message to the channel with embed
            greeting_embed = discord.Embed(title="Hello, I'm ready to work!", description=f"Current time: {current_time}", color=0x00ff00)

            await channel.send(embed=greeting_embed)
        else:
            # send message to the channel saying that the bot is not ready
            channel = self.get_channel(CHANNEL_ID)

            # get current date and time under the nice format
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # send message to the channel with embed
            greeting_embed = discord.Embed(title="Hello, I'm not ready to work!", description=f"Current time: {current_time}", color=0xff0000)

            await channel.send(embed=greeting_embed)


# set up client and command tree
client = Client()

# run the bots
client.run(BOT_TOKEN)