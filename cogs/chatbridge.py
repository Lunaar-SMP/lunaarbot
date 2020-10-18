import discord
import os
from discord.ext import commands, tasks
from discord.utils import get
import mcrcon
from mcrcon import MCRcon

bot = discord.Client()

class test(commands.Cog):

    def __init__(self, bot):
        self.client = bot
        self.minecraft_to_discord.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Chatbridge is online.')

    @commands.Cog.listener()
    async def on_message(self, message):
        guild = message.channel.guild
        bridge_channel = discord.utils.get(guild.text_channels, id=id)
        if message.author.bot == False:
            if message.channel == bridge_channel:
                rcon = MCRcon('ip', 'rcon password', rcon port)
                rcon.connect()
                msg = rcon.command(f'/tellraw @a "[{message.author.name}] {message.content}"')
                rcon.disconnect()

    last_line = ''

    @tasks.loop(seconds=0.5)
    async def minecraft_to_discord(self):
        with open ('C:/Users/name/path/file/logs/latest.log', 'rb') as f:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            last_line = f.readline().decode()
            if last_line != self.last_line:
                self.last_line = last_line
                guild = self.client.get_guild()#idk the nane of what goes in the ()
                if guild != None:
                    bridge_channel = discord.utils.get(guild.text_channels, id=id goes here)
                    if 'Rcon' not in (last_line.partition(']:')[2]).strip():
                        if 'join the game' or 'left the game' in last_line:
                            if bridge_channel:
                                await bridge_channel.send((last_line.partition(']:')[2]).strip())
                        elif '>' in last_line:
                            if bridge_channel:
                                await bridge_channel.send((last_line.partition(']:')[2]).strip())

def setup(bot):
    bot.add_cog(test(bot))
