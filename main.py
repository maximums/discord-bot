import os
from discord import ChannelType, FFmpegPCMAudio, VoiceClient
from discord.ext import commands
from discord.abc import GuildChannel

TOKEN = 'OTk2MDgxNTgwNjA0OTIzOTI0.G9dsNv.R0WfixVUvoAk7HU-5dkYvdcR4X0CX9SgQ7SVTA'
AKSHAN_DIFF = "https://www.youtube.com/watch?v=8EsQy-C2ZCQ"
KAYLE_DIFF = "https://www.youtube.com/watch?v=R9USJ4Cruuk"
SION_DIFF = "https://www.youtube.com/watch?v=0HjROUHWG9M"

client = commands.Bot(command_prefix=';')

@client.event
async def on_ready():
    text_channels = _get_channels_by_type(ChannelType.text)
    voice_channels = _get_channels_by_type(ChannelType.voice)
    await voice_channels[2].connect()
    # await text_channels[1].send("Ready")
    # await text_channels[1].send("Available commands:\n\t\t\t\t\t\t\t:zdarova, :akshan, :sion, :kayle\nEx.: type in any channel chat ':akshan'")
    for channel in text_channels:
        await channel.send("Ready for work😅")
        await channel.send("Available commands:\n\t\t\t\t\t\t\t:akshan, :sion, :kayle\nEx.: type in any channel chat ':akshan'")

@client.command(name="akshan")
async def _akshan_diff(ctx):
    await ctx.send("{} it's for you buddy:\n{}".format(ctx.author.name, AKSHAN_DIFF))

@client.command(name="sion")
async def _sion_diff(ctx):
    await ctx.send("{} it's for you buddy:\n{}".format(ctx.author.name, SION_DIFF))

@client.command(name="kayle")
async def _kayle_diff(ctx):
    await ctx.send("{} it's for you buddy:\n{}".format(ctx.author.name, KAYLE_DIFF))

@client.command()
async def zdarova(ctx):
    author_channel: GuildChannel = ctx.message.author.voice.channel
    v_client: VoiceClient = client.voice_clients[0]
    if not v_client.is_connected():
        v_client = await author_channel.connect()
    await v_client.move_to(author_channel)
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'audio/r2.opus')
    source = FFmpegPCMAudio(filename)
    v_client.play(source)


def _get_channels_by_type(type: ChannelType):
    return [channel for guild in client.guilds for channel in guild.channels if channel.type == type]

client.run(TOKEN)