import asyncio
import datetime
from discord.utils import get
import json

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
        self.rcon_smp = MCRcon(config_rcon['rcon_smp']['rcon-ip'], config_rcon['rcon_smp']['rcon-password'], config_rcon['rcon_smp']['rcon-port'])
        self.coords = ()
        self.peri_size = 0
        self.worldeater_crashed = False
        self.we_updates = False

    @commands.Cog.listener()
    async def on_ready(self):
        print('World eater commands is online.')
        self.guild = self.client.get_guild(config_rcon['guild'])
        self.we_channel = discord.utils.get(self.guild.text_channels, id=config_discord["worldeater_channel"])

    @commands.command(help='use this to start the worldeater script. Arguments: peri_size , optional<x,z>. x and z argument: random position in the peri for height control')
    @commands.has_any_role('Member', 'Trial-Member')
    async def westart(self, ctx, peri_size: int, *coords):
        if self.check_worldeater.is_running():
            await ctx.send(
                embed=discord.Embed(
                    title='World eater is already running',
                    color=0xFF0000))
            return
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

    @commands.command(help='stops the world eater script')
    @commands.has_any_role('Member', 'Trial-Member')
    async def westop(self, ctx):
        if not self.check_worldeater.is_running():
            await ctx.send(
                embed=discord.Embed(
                    title='No world eater is running',
                    color=0xFF0000))
            return
        self.check_worldeater.cancel()
        self.check_worldeater.stop()
        self.coords = ()
        self.peri_size = 0
        self.worldeater_crashed = False
        self.we_updates = False
        await ctx.send(embed=discord.Embed(
            title=f'World eater script is stopped now',
            colour=0x00FF00,
        ))

    @commands.command(help='use this to get info about the world eater')
    @commands.has_any_role('Member', 'Trial-Member')
    async def westatus(self, ctx):
        if not self.check_worldeater.is_running():
            await ctx.send(
                embed=discord.Embed(
                    title='No world eater is running',
                    color=0xFF0000))
            return

        if self.worldeater_crashed:
            title = 'World eater is stuck'
            color = 0xFF0000
        else:
            title = 'World eater is running'
            color = 0x00FF00

        if not self.coords:
            msg = 'You are running without height control'
        else:
            self.rcon_smp.connect()
            resp = self.rcon_smp.command(f'/script run top(\'surface\',{self.coords[0]}, 0, {self.coords[1]})')
            yLevel = int(resp.split()[1]) + 1
            timeleft = str(datetime.timedelta(seconds=(self.peri_size / 2) * yLevel))
            msg = f'y-level: ~{yLevel}\n' \
                  f'WE has to run for another ~{timeleft}'
            self.rcon_smp.disconnect()
        await ctx.send(embed=discord.Embed(
            title=title,
            colour=color,
            description=msg
        ))

    @commands.command(help='get or remove worldeater role. you get pinged if worldeater crashes')
    @commands.has_any_role('Member', 'Trial-Member')
    async def wehelper(self, ctx):
        we_role = get(self.guild.roles, name=config_discord['worldeater_role'])
        if not we_role in ctx.message.author.roles:
            await ctx.message.author.add_roles(we_role)
            await ctx.send('You now get pinged if a world eater crashes')
        else:
            await ctx.message.author.remove_roles(we_role)
            await ctx.send('You are no longer a world eater helper')

    @commands.command(help = 'get live updates on world eater progress')
    @commands.has_any_role('Member', 'Trial-Member')
    async def weupdates(self, ctx):
        if not self.check_worldeater.is_running():
            await ctx.send(
                embed=discord.Embed(
                    title='No world eater is running',
                    color=0xFF0000))
            return
        if self.we_updates:
            await ctx.send(
                embed=discord.Embed(
                    title='Live updates turned off',
                    color=0xFF0000))
        else:
            await ctx.send(
                embed=discord.Embed(
                    title='Live updates turned on',
                    color=0x00FF00))
        self.we_updates = not self.we_updates

    @tasks.loop()
    async def check_worldeater(self):
        self.rcon_smp.connect()
        resp = self.rcon_smp.command(f'/script run reduce(last_tick_times(),_a+_,0)/100;')
        resp = float(resp.split()[1])
        if resp < 30:
            if not self.worldeater_crashed:
                await asyncio.sleep(10)
                self.rcon_smp.connect()
                resp = self.rcon_smp.command(f'/script run reduce(last_tick_times(),_a+_,0)/100;')
                resp = float(resp.split()[1])
                if resp < 30:
                    role = get(self.guild.roles, name=config_discord['worldeater_role'])
                    await self.we_channel.send(f'{role.mention} World eater is stuck.')
                    self.worldeater_crashed = True
                    self.check_worldeater.change_interval(seconds=10)
        elif self.worldeater_crashed:
            self.worldeater_crashed = False
            self.check_worldeater.change_interval(seconds=self.peri_size / 2)
            await self.we_channel.send(f'World eater is fine again.')
        if(self.we_updates and not self.worldeater_crashed):
            if not self.coords:
                msg = 'still running'
            else:
                self.rcon_smp.connect()
                resp = self.rcon_smp.command(f'/script run top(\'surface\',{self.coords[0]}, 0, {self.coords[1]})')
                yLevel = int(resp.split()[1]) + 1
                timeleft = str(datetime.timedelta(seconds=(self.peri_size / 2) * yLevel))
                msg = f'y-level: ~{yLevel}\n' \
                      f'WE has to run for another ~{timeleft}'
                self.rcon_smp.disconnect()
            await self.we_channel.send(embed=discord.Embed(
                title='WE Updates',
                colour=0x00FF00,
                description=msg
            ))
        self.rcon_smp.disconnect()



def setup(client):
    client.add_cog(worldeatercommands(client))
