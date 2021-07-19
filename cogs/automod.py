from discord.utils import get
import json
import asyncio

import discord
from discord.ext import commands

client = discord.Client()

with open('./config/discord.json') as json_file:
    config_discord = json.load(json_file)

class autoMod(commands.Cog):

    def __init__(self, client):
        self.guild = None
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx, message):
        staff_channel = client.get_channel(config_discord['staff_channel'])
        Illegal = ("Faggot", "Nig", "Nigga", "Nigger", "Fag")
        mute = get(self.guild.roles, name=config_discord['muted'])
        if Illegal in message.content.lower():
            await ctx.message.delete()
            await ctx.message.author.add_roles(mute)
            await staff_channel.send(content='<@&702217128069169152> someone is being racist or saying slurs')

    @client.event
    async def on_ready(self):
        print("Automod is ready")
        while True:
            print("Cleared File")
            await asyncio.sleep(10)
            with open("spam_detect.txt", "r+") as file:
                file.truncate(0)

    @client.event
    async def on_message(self, message):
        counter = 0
        with open("spam_detect.txt", "r+") as file:
            for lines in file:
                if lines.strip("\n") == str(message.author.id):
                    counter+=1

                file.writelines(f"{str(message.author.id)}\n")
                if counter > 7:
                    await message.guild.ban(message.author, reason="spam")

    #@client.event
    #async def on_message(self, message):
        #pings = 0
        #with open("spam_detect.txt", "r+") as file:
            #for lines in file:
                #if lines.strip("\n") == str(message.author.id):
                    #pings+=1

                #file.writelines(f"{str(message.author.id)}\n")
                #if pings > 4:
                    #await message.guild.ban(message.author, reason="pings")

def setup(client):
    client.add_cog(autoMod(client))