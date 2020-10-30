import json
import os
import time

import discord
from discord.ext import commands, tasks
from mcrcon import MCRcon

client = discord.Client()

with open('./config/chatbridge.json') as json_file:
    config = json.load(json_file)

class chatbridge(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.rcon_smp = MCRcon(config['rcon_smp']['rcon-ip'], config['rcon_smp']['rcon-password'], config['rcon_smp']['rcon-port'])
        self.rcon_smp.connect()
        self.line_smp = list(open(config['smp']['latest.log']))[-1][:-1]
        self.rcon_cmp = MCRcon(config['rcon_cmp']['rcon-ip'], config['rcon_cmp']['rcon-password'], config['rcon_cmp']['rcon-port'])
        self.rcon_cmp.connect()
        self.line_cmp = list(open(config['cmp']['latest.log']))[-1][:-1]
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
                self.rcon_smp.command(_message)
                self.rcon_cmp.command(_message)
            else:
                _message = '/tellraw @a ' +  '["[",{"text":' + '"{}"'.format(author) + ',"color":"aqua"}, "] ",' + '{"text":' + '"{}"'.format(message.content) + ',"color":"white"}]'
                self.rcon_smp.command(_message)
                self.rcon_cmp.command(_message)

    @tasks.loop(seconds=0.01)
    async def minecraft_to_discord(self):
        #smp
        with open(config['smp']['latest.log'], 'rb') as log_file:
            log_file.seek(-2, os.SEEK_END)
            while log_file.read(1) != b'\n':
                log_file.seek(-2, os.SEEK_CUR)
            line_smp = log_file.readline().decode()[:-2]
            if self.line_smp != line_smp:
                self.line_smp = line_smp
                if '<' == line_smp[33]:
                    message = (line_smp.partition(']:')[2]).replace('<', '', 1).replace('>', ':', 1)[1:]
                    await self.bridge_channel.send('[SMP] ' + message)
                    cmd = '/tellraw @a ' + '["[",{"text":' + '"{}"'.format(message.partition(':')[0]) + ',"color":"red"}, "] ",' + '{"text":' + '"{}"'.format(message.partition(':')[2][1:]) + ',"color":"white"}]'
                    self.rcon_cmp.command(cmd)

                elif 'the game' in line_smp and not 'Sav' in line_smp:
                    await self.bridge_channel.send(line_smp.partition(']:')[2][:-4] + 'SMP')

        #cmp
        with open(config['cmp']['latest.log'], 'rb') as log_file:
            log_file.seek(-2, os.SEEK_END)
            while log_file.read(1) != b'\n':
                log_file.seek(-2, os.SEEK_CUR)
            line_cmp = log_file.readline().decode()[:-2]
            if self.line_cmp != line_cmp:
                self.line_cmp = line_cmp
                if '<' == line_cmp[33]:
                    message = (line_cmp.partition(']:')[2]).replace('<', '', 1).replace('>', ':', 1)[1:]
                    await self.bridge_channel.send('[CMP] ' +message)
                    cmd = '/tellraw @a ' + '["[",{"text":' + '"{}"'.format(message.partition(':')[0]) + ',"color":"red"}, "] ",' + '{"text":' + '"{}"'.format(message.partition(':')[2][1:]) + ',"color":"white"}]'
                    self.rcon_smp.command(cmd)
                elif 'the game' in line_cmp and not 'Sav' in line_cmp:
                    await self.bridge_channel.send(line_cmp.partition(']:')[2][:-4] + 'CMP')

def setup(client):
    client.add_cog(chatbridge(client))

