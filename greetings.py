import discord
import os
from discord.ext import commands

_dirname = os.path.dirname(__file__)
_IMG = os.path.join(_dirname, 'loli.gif')

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')
            await channel.send(file=discord.File(_IMG))

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.name}~')
            await ctx.send(file=discord.File(_IMG))
        else:
            await ctx.send(f'Hello {member.name}... This feels familiar.')
            await ctx.send(file=discord.File(_IMG))
        self._last_member = member
