import discord
from discord.ext import commands
import asyncio

client = discord.Client()

class autoMod(commands.Cog):

    def __init__(self, client):
        self.guild = None
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            await asyncio.sleep(10)
            with open("spam_detect.txt", "r+") as file:
                file.truncate(0)
            with open("ping_detect.txt", "r+") as file:
                file.truncate(0)

    @commands.Cog.listener(name="on_message")
    async def _blacklisted_word(self, message: discord.Message) -> None:
        pass
        if any(i in message.content for i in ("fag", "nig", "nigga", "faggot", "nigger", "trany")):
            await message.guild.ban(message.author, reason="slur")

    @commands.Cog.listener(name="on_message")
    async def _spam(self, message: discord.Message) -> None:
        pass
        counter = 0
        with open("spam_detect.txt", "r+") as file:
            for lines in file:
                if lines.strip("\n") == str(message.author.id):
                    counter += 1

            file.writelines(f"{str(message.author.id)}\n")
            if counter > 5:
                await message.guild.ban(message.author, reason="spam")

    @commands.Cog.listener(name="on_message")
    async def _pings(self, message: discord.Message):
        if len(message.mentions) > 5:
            await message.guild.ban(message.author, reason="pings")

def setup(client):
    client.add_cog(autoMod(client))