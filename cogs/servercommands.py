import json
import discord
from discord.ext import commands
from mcrcon import MCRcon


client = discord.Client()

with open('./config/chatbridge.json') as json_file:
    config_rcon = json.load(json_file)

with open('./config/discord.json') as json_file:
    config_discord = json.load(json_file)

class servercommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.rcon_smp = MCRcon(config_rcon['rcon_smp']['rcon-ip'], config_rcon['rcon_smp']['rcon-password'], config_rcon['rcon_smp']['rcon-port'])
        self.rcon_cmp = MCRcon(config_rcon['rcon_cmp']['rcon-ip'], config_rcon['rcon_cmp']['rcon-password'], config_rcon['rcon_cmp']['rcon-port'])
        self.rcon_mirror = MCRcon(config_rcon['rcon_mirror']['rcon-ip'], config_rcon['rcon_mirror']['rcon-password'], config_rcon['rcon_mirror']['rcon-port'])

    @commands.Cog.listener()
    async def on_ready(self):
        print('Servercommands is online.')

    @commands.command(help = 'All server commands can be used with the format: !execute command. For example, !execute whitelist notch. Note that only members with the role Admin can use this command.(SMP)')
    @commands.has_role(config_discord['admin_role'])
    async def execute_smp(self, ctx, *, command):
        self.rcon_smp.connect()
        resp = self.rcon_smp.command(f'/{command}')
        if resp:
            await ctx.send(f'```{resp}```')

    @commands.command(
        help='All server commands can be used with the format: !execute command. For example, !execute whitelist notch. Note that only members with the role Admin can use this command.(CMP)')
    @commands.has_role(config_discord['admin_role'])
    async def execute_cmp(self, ctx, *, command):
        self.rcon_cmp.connect()
        resp = self.rcon_cmp.command(f'/{command}')
        if resp:
            await ctx.send(f'```{resp}```')

    @commands.command(help = 'All server commands can be used with the format: !execute command. For example, !execute whitelist notch. Note that only members with the role Admin can use this command.(Mirror)')
    @commands.has_role(config_discord['admin_role'])
    async def execute_mirror(self, ctx, *, command):
        self.rcon_mirror.connect()
        resp = self.rcon_mirror.command(f'/{command}')
        if resp:
            await ctx.send(f'```{resp}```')

    @commands.command(help = 'Tells who is online')
    async def online(self, ctx):
        embed = discord.Embed(
            title='Online players',
            colour=0xFEFEFE
        )
        embed.set_footer(
            text=f'Requested by {ctx.message.author.name}',
            icon_url=ctx.message.author.avatar_url
        )
        try:
            self.rcon_smp.connect()
            players_smp = self.rcon_smp.command(f'list').partition(': ')[2].split()
            embed.add_field(name=f'SMP: {len(players_smp)}',
                            value='\n'.join(players_smp) if len(players_smp) > 0 else '\u200b',
                            inline=True
                            )
        except:
            embed.add_field(name='SMP is offline',
                            value='\u200b',
                            inline=True
                            )

        try:
            self.rcon_cmp.connect()
            players_cmp = self.rcon_cmp.command(f'list').partition(': ')[2].split()
            embed.add_field(name=f'CMP: {len(players_cmp)}',
                            value='\n'.join(players_cmp) if len(players_cmp) > 0 else '\u200b',
                            inline=True
                            )
        except:
            embed.add_field(name='CMP is offline',
                            value='\u200b',
                            inline=True
                            )

        try:
            self.rcon_mirror.connect()
            players_mirror = self.rcon_mirror.command(f'list').partition(': ')[2].split()
            embed.add_field(name=f'SMP: {len(players_mirror)}',
                            value='\n'.join(players_mirror) if len(players_mirror) > 0 else '\u200b',
                            inline=True
                            )
        except:
            embed.add_field(name='Mirror is offline',
                            value='\u200b',
                            inline=True
                            )

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(servercommands(client))
