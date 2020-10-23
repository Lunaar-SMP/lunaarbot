import tailer
import json
import discord
from discord.ext import commands, tasks
from discord.utils import get
import mcrcon
from mcrcon import MCRcon

client = discord.Client()

with open('./chatbridge/chatbridge.json') as json_file:
    config = json.load(json_file)

class chatbridge(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.rcon = MCRcon(config['rcon']['rcon-ip'], config['rcon']['rcon-password'], config['rcon']['rcon-port'])
        self.rcon.connect()
        self.line = tailer.tail(open(config['minecraft_to_discord']['latest.log']), 1)[1]
        self.minecraft_to_discord.start()

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.client.get_guild(config['guild'])
        self.bridge_channel = discord.utils.get(self.guild.text_channels, id=config['bridge_channel'])

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel == self.bridge_channel and message.author.bot == False:
            if message.author.nick != None:
                author = message.author.nick
            else:
                author = message.author.name
            
            if message.attachments:
                _message = '/tellraw @a ' +  '["[",{"text":' + '"{}"'.format(author) + ',"color":"aqua"}, "] ",'
                for attachment in message.attachments:
                    _message = _message + '{"text":' + '"{}"'.format(attachment.filename) + ',"clickEvent":{"action":"open_url", "value":' + '"{}"'.format(attachment.url) + '}, "hoverEvent": {"action":"show_text", "value":"Click to open in your web browser"}, "color": "green"}'
                _message = _message + ']'
                self.rcon.command(_message)
            else:
                _message = '/tellraw @a ' +  '["[",{"text":' + '"{}"'.format(author) + ',"color":"aqua"}, "] ",' + '{"text":' + '"{}"'.format(message.content) + ',"color":"white"}]'
                self.rcon.command(_message)

    @tasks.loop(seconds=0.01)
    async def minecraft_to_discord(self):
        line = tailer.tail(open(config['minecraft_to_discord']['latest.log']), 1)[1]
        if self.line != line:
            self.line = line
            if '>' in line:
                await self.bridge_channel.send((line.partition(']:')[2]).replace('<', '').replace('>', ':'))
            elif 'the game' in line:
                await self.bridge_channel.send(line.partition(']:')[2])

def setup(client):
    client.add_cog(chatbridge(client))

