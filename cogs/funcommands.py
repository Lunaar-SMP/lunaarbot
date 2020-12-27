import discord
from discord.ext import commands


client = discord.Client()

class funcommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('funcommands is online.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if 'is broken' in message.content.lower():
            await message.channel.send('but <@624586193979441183> repaired it')

def setup(client):
    client.add_cog(funcommands(client))
