import json
import discord
from discord.ext import commands
from mcrcon import MCRcon


client = discord.Client()

with open('./config/rcon.json') as json_file:
    config_rcon = json.load(json_file)

with open('./config/discord.json') as json_file:
    config_discord = json.load(json_file)

class servercommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.servers = {'SMP': MCRcon(config_rcon['rcon_smp']['rcon-ip'], config_rcon['rcon_smp']['rcon-password'], config_rcon['rcon_smp']['rcon-port']),
                        'CMP': MCRcon(config_rcon['rcon_cmp']['rcon-ip'], config_rcon['rcon_cmp']['rcon-password'], config_rcon['rcon_cmp']['rcon-port']),
                        'Mirror': MCRcon(config_rcon['rcon_mirror']['rcon-ip'], config_rcon['rcon_mirror']['rcon-password'], config_rcon['rcon_mirror']['rcon-port']),
                        'Testcreative': MCRcon(config_rcon['rcon_testcreative']['rcon-ip'], config_rcon['rcon_testcreative']['rcon-password'], config_rcon['rcon_testcreative']['rcon-port'])}

    @commands.Cog.listener()
    async def on_ready(self):
        print('Servercommands is online.')

    @commands.command(
        help='All server commands can be used with the format: !execute command. For example, !execute whitelist notch. Note that only members with the role Admin can use this command.(CMP)')
    @commands.has_role(config_discord['admin_role'])
    async def execute(self, ctx, server, * , command):
        for k, v in self.servers.items():
            if k.lower() == server.lower():
                try:
                    v.connect()
                    resp = v.command(f'/{command}')
                    v.disconnect()
                    if resp:
                        await ctx.send(f'```{resp}```')
                        return
                except:
                    await ctx.send('Server offline')
                    return
        await ctx.send(f'No server **{server}** found')

    @commands.command(help = 'whitelist all')
    @commands.has_role(config_discord['admin_role'])
    async def whitelist(self, ctx, parameter, name=None):
        embed = discord.Embed(
            title='Whitelist all',
            colour=0xFEFEFE
        )
        embed.set_footer(
            text=f'Requested by {ctx.message.author.name}',
            icon_url=ctx.message.author.avatar_url
        )
        command = "/whitelist {}" .format(parameter + ' ' + name if name else parameter)
        for k, v in self.servers.items():
            try:
                v.connect()
                resp = v.command(command)
                v.disconnect()
                if resp:
                    embed.add_field(name=k,
                                    value=resp,
                                    inline=True
                                    )
            except:
                embed.add_field(name=f'{k} is offline',
                                value='\u200b',
                                inline= True
                                )

        await ctx.send(embed=embed)

    @commands.command(help = 'Tells who is online', aliases=['o'])
    async def online(self, ctx):
        embed = discord.Embed(
            title='Online players',
            colour=0xFEFEFE
        )
        embed.set_footer(
            text=f'Requested by {ctx.message.author.name}',
            icon_url=ctx.message.author.avatar_url
        )
        for k, v in self.servers.items():
            try:
                v.connect()
                players = v.command(f'list').partition(': ')[2].split()
                v.disconnect()
                embed.add_field(name=f'{k}: {len(players)}',
                                value='\n'.join(players) if len(players) > 0 else '\u200b',
                                inline=True
                                )
            except:
                embed.add_field(name=f'{k} is offline',
                                value='\u200b',
                                inline=True
                                )

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(servercommands(client))
