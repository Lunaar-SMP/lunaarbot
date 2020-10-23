import discord
import os
from discord.ext import commands, tasks
from mcrcon import MCRcon

client = discord.Client()


class chatbridge(commands.Cog):

    def __init__(self, bot):
        self.client = bot
        self.minecraft_to_discord.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Chatbridge is online.')

    @commands.Cog.listener()
    async def on_message(self, message):
        guild = message.channel.guild
        bridge_channel = discord.utils.get(guild.text_channels, id=769171806799659018)
        if message.author.bot == False:
            if message.channel == bridge_channel:
                rcon = MCRcon('127.0.0.1', '12345', 25575)
                rcon.connect()
                msg = rcon.command(f'/tellraw @a "[{message.author.name}] {message.content}"')
                rcon.disconnect()

    last_line = ''

    @tasks.loop(seconds=0.5)
    async def minecraft_to_discord(self):
        with open('D:/McServer/testing server/logs/latest.log', 'rb') as f:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            last_line = f.readline().decode()
            if last_line != self.last_line:
                self.last_line = last_line
                guild = self.client.get_guild(192972603579695104)  # idk the nane of what goes in the ()
                if guild is not None:
                    bridge_channel = discord.utils.get(guild.text_channels, id=769171806799659018)
                    msg = (last_line.partition(']:')[2]).strip()
                    if bridge_channel:
                        if '>' in msg and '<' in msg:
                            msg = msg.replace('<', '**<', 1)
                            msg = msg.replace('>', '>**', 1)
                            await bridge_channel.send(msg)
                        elif 'joined the game' in msg or 'left the game' in msg:
                            await bridge_channel.send(msg)


def setup(bot):
    bot.add_cog(chatbridge(bot))
