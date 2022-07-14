import os
from discord import ChannelType, FFmpegPCMAudio, VoiceClient
from discord.ext import commands
from discord.abc import GuildChannel
from greetings import Greetings
from music import MusicCog

TOKEN = 'OTk2MDgxNTgwNjA0OTIzOTI0.G9dsNv.R0WfixVUvoAk7HU-5dkYvdcR4X0CX9SgQ7SVTA'
AKSHAN_DIFF = "https://www.youtube.com/watch?v=8EsQy-C2ZCQ"
KAYLE_DIFF = "https://www.youtube.com/watch?v=R9USJ4Cruuk"
SION_DIFF = "https://www.youtube.com/watch?v=0HjROUHWG9M"

client = commands.Bot(command_prefix=';')
client.add_cog(MusicCog(client))
client.add_cog(Greetings(client))

@client.event
async def on_ready():
    text_channels = _get_channels_by_type(ChannelType.text)
    voice_channels = _get_channels_by_type(ChannelType.voice)
    await voice_channels[2].connect()
    await text_channels[1].send("Ready")
    # for channel in text_channels:
    #     await channel.send("Ready for work😅")
    #     await channel.send("""Available commands:
    #     ;akshan - Youtube video,
    #     ;sion - Youtube video,
    #     ;kayle - Youtube video "
    #     ;add 'video title' - adding song from YouTube to playlist
    #     ;play - stat play music from playlist[it should not be empty]
    #     ;hello - Hello message and img"
    #     Ex.: type in any channel chat ';akshan'""")

@client.command(name="akshan")
async def _akshan_diff(ctx):
    await ctx.send("{} it's for you buddy:\n{}".format(ctx.author.name, AKSHAN_DIFF))

@client.command(name="sion")
async def _sion_diff(ctx):
    await ctx.send("{} it's for you buddy:\n{}".format(ctx.author.name, SION_DIFF))

@client.command(name="kayle")
async def _kayle_diff(ctx):
    await ctx.send("{} it's for you buddy:\n{}".format(ctx.author.name, KAYLE_DIFF))

def _get_channels_by_type(type: ChannelType):
    return [channel for guild in client.guilds for channel in guild.channels if channel.type == type]

client.run(TOKEN)