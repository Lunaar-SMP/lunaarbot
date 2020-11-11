import json
import discord
from discord.ext import commands
from mcrcon import MCRcon
import time

client = discord.Client()

with open('./config/chatbridge.json') as json_file:
    config_rcon = json.load(json_file)

with open('./config/discord.json') as json_file:
    config_discord = json.load(json_file)

class worldeatercommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.rcon_smp = MCRcon(config_rcon['rcon_smp']['rcon-ip'], config_rcon['rcon_smp']['rcon-password'],config_rcon['rcon_smp']['rcon-port'])

    @commands.Cog.listener()
    async def on_ready(self):
        print('World eater commands is online.')

    @commands.command(help = 'use this to start the worldeater script')
    @commands.has_any_role('Member', 'Trial-Member')
        async def westart(self, ctx, *, *):
            self.rcon_smp.connect()
            resp = self.rcon_smp.command(f'/script run reduce(last_tick_times(),_a+_,0)/100;')
            resp = float(resp.split()[1])
            if resp < 30:
                asyncio.sleep(10)
                self.rcon_smp.connect()
                resp = self.rcon_smp.command(f'/script run reduce(last_tick_times(),_a+_,0)/100;')
                resp = float(resp.split()[1])
                if resp < 30:
                    await.ctx.send(f'World eater is stuck.')
                    if else:
                        await ctx.send(f'World eater is fine')

    @commands.command(help = 'get or remove worldeater role. you get pinged if worldeater crashes')
    @commands.has_any_role('Member', 'Trial-Member')
    async def wehelperadd(self, ctx):
        await ctx.message.author.add_roles('Worldeaterhelper')
        await ctx.send('You now get pinged if a worldeater crashes')

    @commands.Cog.listener()
    async def on_raw_reaction_add(payload):
        if payload.channel_id == 767588796932947991 and payload.message_id == 776120832191102976:
            if str(payload.emoji) == "<:WEHelper:776121112294850591>":
                guild = client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = get(payload.member.guild.roles, name = 'WE Helper')
        await payload.member.add_roles(role)







def setup(client):
    client.add_cog(worldeatercommands(client))
