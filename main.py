import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix='!', case_insensitive=True)

log_channel_id = 769171777338474496

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command(name = 'restart', help = 'Restarts the bot')
@commands.has_role('Dev')
async def restart(ctx):
    embed = discord.Embed(
    title = f'{client.user.name} restarting!'
    )
    await client.close()

@client.event
async def on_ready():
    print(f'Logged in as {client.user} and connected to Discord! (ID: {client.user.id})')

    game = discord.Game(name = 'chrome remote desktop')
    await client.change_presence(activity = game)

    log_channel = client.get_channel(log_channel_id)
    await log_channel.send(content = 'Bot is online.')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.load_extension('chatbridge.chatbridge')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(embed=discord.Embed(title='You do not have permission to execute this command', color=0xFF0000))

client.run('token', bot = True, reconnect = True)
