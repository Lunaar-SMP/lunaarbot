import discord
from discord.ext import commands
import mcrcon
from mcrcon import MCRcon
import random

client = discord.Client()

class commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Commands is online.')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round((self.client.latency * 1000), 1)}ms')

    @commands.command()
    async def application(self, ctx):
        await ctx.send('https://forms.gle/TVuATxk4rTbH4Eub7')

    @commands.command(aliases = ['8ball'])
    async def _8ball(self, ctx, *, question):
        responses = ["It is certain.",
    "It is decidedly so.",
    "Without a doubt.",
    "Yes - definitely.",
    "You may rely on it.",
    "As I see it, yes.",
    "Most likely.",
    "Outlook good.",
    "Yes.",
    "Signs point to yes.",
    "Reply hazy, try again.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again.",
    "Don't count on it.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Very doubtful."]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command()
    @commands.has_role('Admin')
    async def clear(self, ctx, amount=0):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'Deleted {amount} messages')

    @commands.command()
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)

    @commands.command()
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)

    @commands.command()
    @commands.has_role('Admin')
    async def whitelist(self, ctx, name):
        rcon = MCRcon('ip', 'rcon password', rcon , port)
        rcon.connect()
        msg = rcon.command(f'whitelist add {name}')
        await ctx.send(f'{msg}')

    @commands.command()
    async def online(self, ctx):
        rcon = MCRcon('ip', 'rcon password', rcon , port)
        rcon.connect()
        msg = rcon.command(f'list')
        await ctx.send(f'{msg}')

def setup(client):
    client.add_cog(commands(client))
