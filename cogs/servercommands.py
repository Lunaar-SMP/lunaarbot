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
        players = self.rcon.command(f'list').partition(': ')[2].split()
        print(players)
        print('\n'.join(players))
        embed = discord.Embed(
            title=f'Online players: {len(players)}',
            colour=0xFEFEFE,
            description='\n'.join(players)
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(servercommands(client))
