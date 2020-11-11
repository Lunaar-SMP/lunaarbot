import asyncio
import datetime
import json
import time
from asyncio import Task

import discord
from discord.ext import commands, tasks
from mcrcon import MCRcon


client = discord.Client()

with open('./config/chatbridge.json') as json_file:
    config_rcon = json.load(json_file)

with open('./config/discord.json') as json_file:
    config_discord = json.load(json_file)


class worldeatercommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.rcon_smp = MCRcon(config_rcon['rcon_smp']['rcon-ip'], config_rcon['rcon_smp']['rcon-password'],config_rcon['rcon_smp']['rcon-port'])
        self.coords = ()
        self.peri_size = 0
        self.worldeater_crashed = False

    @commands.Cog.listener()
    async def on_ready(self):
        print('World eater commands is online.')
        self.guild = self.client.get_guild(767498295319986178)
        self.we_channel = discord.utils.get(self.guild.text_channels, id=767588796932947991)

    @commands.command(help = 'use this to start the worldeater script')
    @commands.has_any_role('Member', 'Trial-Member', 'Dev')
    async def westart(self, ctx, peri_size: int, *coords):
        self.peri_size = peri_size
        if len(coords) == 2:
            self.coords = coords
            msg = f'The peri size is: {peri_size}\n' \
                  f'Coordinates for height control: x={coords[0]} y={coords[1]}'
        else:
            self.coords = ()
            msg = f'The peri size is: {peri_size}\n' \
                  f'You are running without height control'
        cycletime = peri_size / 2
        self.check_worldeater.change_interval(seconds=cycletime)
        self.check_worldeater.start()
        embed = discord.Embed(
            title=f'WE script is running now',
            colour=0xFEFEFE,
            description=msg
        )
        await ctx.send(embed=embed)

    @commands.command(help = 'stops the worldeater script')
    @commands.has_any_role('Member', 'Trial-Member', 'Dev')
    async def westop(self, ctx):
        if not self.check_worldeater.is_running():
            await ctx.send(
                embed=discord.Embed(
                    title='No world eater is running',
                    color=0xFF0000))
            return
        self.check_worldeater.cancel()
        self.check_worldeater.stop()
        await ctx.send(embed = discord.Embed(
            title=f'World eater script is stopped now',
            colour=0x00FF00,
        ))

    @commands.command(help = 'get or remove worldeater role. you get pinged if worldeater crashes')
    @commands.has_any_role('Member', 'Trial-Member')
    async def wehelperadd(self, ctx):
        await ctx.message.author.add_roles('Worldeaterhelper')
        await ctx.send('You now get pinged if a worldeater crashes')

    #@commands.Cog.listener()
    #async def on_raw_reaction_add(payload):
    #    if payload.channel_id == 767588796932947991 and payload.message_id == 776120832191102976:
    #        if str(payload.emoji) == "<:WEHelper:776121112294850591>":
    #            guild = client.get_guild(payload.guild_id)
    #    member = guild.get_member(payload.user_id)
    #    role = get(payload.member.guild.roles, name = 'WE Helper')
    #    await payload.member.add_roles(role)
#
    @tasks.loop()
    async def check_worldeater(self):
        print(f'Loop: {time.localtime()}')
        self.rcon_smp.connect()
        resp = self.rcon_smp.command(f'/script run reduce(last_tick_times(),_a+_,0)/100;')
        resp = float(resp.split()[1])
        if resp < 30:
            if not self.worldeater_crashed:
                await asyncio.sleep(10)
                print(f'Wait: {time.localtime()}')
                self.rcon_smp.connect()
                resp = self.rcon_smp.command(f'/script run reduce(last_tick_times(),_a+_,0)/100;')
                resp = float(resp.split()[1])
                if resp < 30:
                    await self.we_channel.send(f'World eater is stuck.')
                    self.worldeater_crashed = True
        elif self.worldeater_crashed:
            self.worldeater_crashed = False
            await self.we_channel.send(f'World eater is fine again.')
        self.rcon_smp.disconnect()


def setup(client):
    client.add_cog(worldeatercommands(client))
