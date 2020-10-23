import json

import discord
from discord.ext import commands
from mcrcon import MCRcon
import subprocess

client = discord.Client()

with open('./config/chatbridge.json') as json_file:
    config = json.load(json_file)

class servercommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.rcon = MCRcon(config['rcon']['rcon-ip'], config['rcon']['rcon-password'], config['rcon']['rcon-port'])

    @commands.Cog.listener()
    async def on_ready(self):
        print('Servercommands is online.')

    @commands.command(help = 'All server commands can be used with the format: !execute command. For example, !execute whitelist notch. Note that only members with the role Admin can use this command.')
    @commands.has_role('Dev')
    async def execute(self, ctx, *, command):
        self.rcon.connect()
        resp = self.rcon.command(f'/{command}')
        if resp:
            await ctx.send(f'```{resp}```')

    @commands.command(help = 'Tells who is online')
    async def online(self, ctx):
        self.rcon.connect()
        msg = self.rcon.command(f'list')
        print(msg)
        embed = discord.Embed(colour=discord.member.color, timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=discord.member.avatar_url)
        embed.add_field(name=f'({len(msg)})' " players online: ", value=msg)
        await ctx.send(embed=embed)
        #await ctx.send(f'{msg}')

    @commands.command()
    @commands.has_role('Dev')
    async def startserver(self, ctx):
        subprocess.call([r'C:/Users/tyler/Desktop/1.15.2_Server/start.bat'])

def setup(client):
    client.add_cog(servercommands(client))
