import json
import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix='!', case_insensitive=True)
client.remove_command('help')

with open('./config/discord.json') as json_file:
    config = json.load(json_file)

@client.command()
@commands.has_role(config['admin_role'])
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'loaded {extension}')

@client.command()
@commands.has_role(config['admin_role'])
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'unloaded {extension}')

@client.event
async def on_ready():
    print(f'Logged in as {client.user} and connected to Discord! (ID: {client.user.id})')

    game = discord.Game(name = 'chrome remote desktop')
    await client.change_presence(activity = game)

    log_channel = client.get_channel(config['log_channel'])
    await log_channel.send(content = 'Bot is online.')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(embed=discord.Embed(title='You do not have permission to execute this command', color=0xFF0000))

client.run(config['token'], bot = True, reconnect = True)
