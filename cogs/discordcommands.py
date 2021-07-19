import json
import discord
from discord.ext import commands
import random
from discord.utils import get

client = discord.Client()

with open('./config/discord.json') as json_file:
    config = json.load(json_file)

class discordcommands(commands.Cog):

    def __init__(self, client):
        self.guild = None
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Discordcommands is online.')

    @commands.command(help = 'This commamd tells how much ping the bot has')
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round((self.client.latency * 1000), 1)}ms')

    @commands.command(help = 'Want to apply to Lunaar? Type !application and click the link below')
    async def application(self, ctx):
        await ctx.send('https://forms.gle/TVuATxk4rTbH4Eub7')

    @commands.command(name = '8ball', help = 'Test your fate with the omniscient 8ball')
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

    @commands.command(help = 'This command allows people with the Admin role to clear messages easily')
    @commands.has_role(config['admin_role'])
    async def clear(self, ctx, amount=0):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'Deleted {amount} messages')

    @commands.command(help = 'Admins can kick people with this command')
    @commands.has_role(config['admin_role'])
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)

    @commands.command(help = 'Admins can ban people with this command')
    @commands.has_role(config['admin_role'])
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)

    @commands.command(help = 'Members can use this to mute people. !mute @user reason')
    @commands.has_role('Member')
    async def mute(self, ctx, member : discord.Member, *, reason=None):
        mute_role = get(self.guild.roles, name=config['mute_role'])
        log_channel = client.get_channel(config['log_channel'])
        await member.add_roles(mute_role)
        await log_channel.send(reason=reason)

    @commands.command(help = 'Admins can give roles with this command. To use, type !addrole role @person')
    @commands.has_role(config['admin_role'])
    async def addrole(self, ctx, role : discord.Role, user : discord.Member):
        await user.add_roles(role)
        await ctx.send(f'Gave {role} to {user.mention}.')

    @commands.command(help = 'Admins can remove roles with this command')
    @commands.has_role(config['admin_role'])
    async def removerole(self, ctx, role : discord.Role, user : discord.Member):
        await user.remove_roles(role)
        await ctx.send(f'Removed {role} from {user.mention}.')

def setup(client):
    client.add_cog(discordcommands(client))
