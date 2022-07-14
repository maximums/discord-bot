from discord import ChannelType
from discord.ext import commands
from greetings import Greetings
from music import MusicCog

TOKEN = 'OTk2MDgxNTgwNjA0OTIzOTI0.G9dsNv.R0WfixVUvoAk7HU-5dkYvdcR4X0CX9SgQ7SVTA'
AKSHAN_DIFF = "https://www.youtube.com/watch?v=8EsQy-C2ZCQ"
KAYLE_DIFF = "https://www.youtube.com/watch?v=R9USJ4Cruuk"
SION_DIFF = "https://www.youtube.com/watch?v=0HjROUHWG9M"
COMMANDS = """
            ;add [video title or URL] - adding song from YouTube to playlist(DO NOT SUPPORT PLAYLISTS FROM YOUTUBE!)
            ;play - start play music from playlist[it should not be empty]
            ;hello - Hello message + a kawaii image"
            ;skip - skips current song from playlist
            ;reset - clear playlist and moves Bot to AFK channel
            ;help [command without ';' at the beginning] - display a command description
            ;akshan, ;kayle and ;sion - give YouTube link to funny videos
            """
_FUNNY_VIDEO_HELP = """
                    Usage example:
                    ;akshan
                    ;kayle
                    ;sion
                    Info:
                    Return URL to a funny YouTube video
                    """
_COMMANDS_HELP = """
                 Usage example:
                 ;commands
                 Info:
                 Displays all available commands with short description
                 """

client = commands.Bot(command_prefix=';')
client.add_cog(MusicCog(client))
client.add_cog(Greetings(client))

@client.event
async def on_ready():
    text_channels = _get_channels_by_type(ChannelType.text)
    for channel in text_channels:
        await channel.send("Ready for work😅\nType ;commands in order to see available commands")

@client.command(name="akshan", help=_FUNNY_VIDEO_HELP)
async def _akshan_diff(ctx):
    await ctx.send("{} it's for you buddy:\n{}".format(ctx.author.name, AKSHAN_DIFF))

@client.command(name="sion", help=_FUNNY_VIDEO_HELP)
async def _sion_diff(ctx):
    await ctx.send("{} it's for you buddy:\n{}".format(ctx.author.name, SION_DIFF))

@client.command(name="kayle", help=_FUNNY_VIDEO_HELP)
async def _kayle_diff(ctx):
    await ctx.send("{} it's for you buddy:\n{}".format(ctx.author.name, KAYLE_DIFF))

@client.command(name="commands", help=_COMMANDS_HELP)
async def _available_commands(ctx):
    await ctx.send(COMMANDS)

def _get_channels_by_type(type: ChannelType):
    return [channel for guild in client.guilds for channel in guild.channels if channel.type == type]

client.run(TOKEN)
