from discord import VoiceClient, FFmpegPCMAudio
from discord.ext import commands
from youtube_dl import YoutubeDL

YDL_OPTIONS = {'format': 'bestaudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.music_queue = []

    def search_ytube_item(self, item):
        with YoutubeDL(YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def _play_next(self, client: VoiceClient):
        print('working!!!!')
        if len(self.music_queue) <=0:
            return

        client.play(FFmpegPCMAudio(self.music_queue.pop()['source'], **FFMPEG_OPTIONS), after=lambda e: self._play_next(client))


    @commands.command(name="add", help="Add search song on YouTube and add it to play list")
    async def add_song_to_list(self, ctx, *args):
        if len(args) <= 0:
            await ctx.send("Search query is required")
            return
        
        search_query = " ".join(args)
        song = self.search_ytube_item(search_query)
        self.music_queue.append(song)

    @commands.command()
    async def play(self, ctx):
        voice_channel = ctx.message.author.voice
        if voice_channel is None:
            await ctx.send("{}, you need firts to connect to a voice channel.😅".format(ctx.message.author.name))
            return
        voice_channel = voice_channel.channel
        v_client: VoiceClient = self.bot.voice_clients[0]
        if not v_client.is_connected():
            v_client = await voice_channel.connect()
        await v_client.move_to(voice_channel)

        if len(self.music_queue) <= 0:
            await ctx.send("Empty play list\nPlease add songs to list first")
            return

        song = self.music_queue.pop()
        print(song)
        v_client.play(FFmpegPCMAudio(song['source'], **FFMPEG_OPTIONS), after=lambda e: self._play_next( v_client))

    @commands.command()
    async def skip(ctx):
        pass

