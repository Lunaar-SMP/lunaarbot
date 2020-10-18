import discord
from discord.ext import commands
import random
import os

client = commands.Bot(command_prefix='!', case_insensitive=True)

log_channel_id = client.get_channel(id)

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.event
async def on_ready():
    print(f'Logged in as {client.user} and connected to Discord! (ID: {client.user.id})')
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name='chrome remote desktop'))

    log_channel = client.get_channel(log_channel_id)
    await log_channel.send(content = 'Bot is online.')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(embed=discord.Embed(title='You do not have permission to execute this command', color=0xFF0000))

client.run('token')
