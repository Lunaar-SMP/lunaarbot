import discord
from discord.ext import commands

client = discord.Client()

class helpcommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(help= 'Help command', name='help')
    async def help_command(self, ctx):
        embed = discord.Embed(
            title='Help',
            colour=0xFEFEFE,
            description=''
        )
        embed.set_footer(
            text=f'Requested by {ctx.message.author.name}'
        )

        cogs = list(self.client.cogs.keys())

        for cog in cogs:
            if cog == 'helpcommand':
                continue

            cog_commands = self.client.get_cog(cog).get_commands()
            commands_list = ''
            for comm in cog_commands:
                commands_list += f'\t**{comm.name}** - *{comm.help}*\n'

            if commands_list != '':
                embed.add_field(
                    name=cog,
                    value=commands_list,
                    inline=True
                )

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(helpcommand(client))