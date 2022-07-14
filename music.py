from discord import ChannelType
from discord.ext import commands
from youtube_dl import YoutubeDL
from discord import VoiceClient, FFmpegPCMAudio

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': True}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
_ADD_HELP = """
            Usage example:
            ;add miyagi minor
            ;add [URL to YouTube video]
            Info:
            This command return first video that match your search query or URL
            Also URL should not be to a YouTube playlist
            """
_PLAY_HELP = """
                Usage example:
                ;play
                Info:
                User should be in a voice channel[except AFK channel]
                Bot will connect to user's voice channel and will start play songs from playlist[should not be empty] in reverse oreder.
             """
_SKIP_HELP = """
                Usage example:
                ;skip
                Info:
                Skips current playing song from playlist, if it is last song then stop playing music
             """
_RESET_HELP = """
              Usage example:
              ;reset
              Info:
              Clear playlist and move Bot to AFK voice channel
              """

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing: bool = False
        self.music_queue = []
        self.voice_client: VoiceClient = None

    @commands.Cog.listener()
    async def on_ready(self):
        voice_channels = self._get_channels_by_type(ChannelType.voice)
        self.voice_client = await voice_channels[2].connect()

    @commands.command(name="add", help=_ADD_HELP)
    async def add_song_to_list(self, ctx, *args):
        if len(args) <= 0:
            await ctx.send("Search query is required")
            return
        
        search_query = " ".join(args)
        song = self.search_ytube_item(search_query)
        if song == False:
            await ctx.send("Can't find anything for\n{}".format(search_query))
        self.music_queue.append(song)

    @commands.command(help=_PLAY_HELP)
    async def play(self, ctx):
        if self.is_playing:
            return
            
        voice_channel = ctx.message.author.voice
        if voice_channel is None:
            await ctx.send("{}, you need firts to connect to a voice channel.😅".format(ctx.message.author.name))
            return
        voice_channel = voice_channel.channel

        if self.voice_client is None:
            self.voice_client = await voice_channel.connect()
        else:
            await self.voice_client.move_to(voice_channel)

        if len(self.music_queue) <= 0:
            await ctx.send("Empty play list\nPlease add songs to list first")
            return

        song = self.music_queue.pop()
        self.is_playing = True
        self.voice_client.play(FFmpegPCMAudio(song['source'], **FFMPEG_OPTIONS), after=lambda e: self._play_next())

    @commands.command(help=_SKIP_HELP)
    async def skip(self, ctx):
        if self.voice_client is not None:
            if len(self.music_queue) <= 0:
                await ctx.send("Empty playlist")
                return
            self.voice_client.stop()
            await self.play(ctx)

    @commands.command(help=_RESET_HELP)
    async def reset(self, ctx):
        self.voice_client.stop()
        await self.voice_client.disconnect()
        self.is_playing = False
        self.music_queue = []
        self.voice_client = await self.voice_client.move_to(self._get_channels_by_type(ChannelType.voice)[2])
        await ctx.send('Playlist has been cleared')

    def search_ytube_item(self, item):
        with YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                if item.startswith("https"):
                    info = ydl.extract_info(item, download=False)
                else:
                    info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def _play_next(self):
        if len(self.music_queue) <=0:
            self.is_playing = False
            return
        self.voice_client.play(FFmpegPCMAudio(self.music_queue.pop()['source'], **FFMPEG_OPTIONS), after=lambda e: self._play_next())

    def _get_channels_by_type(self, type: ChannelType):
        return [channel for guild in self.bot.guilds for channel in guild.channels if channel.type == type]

