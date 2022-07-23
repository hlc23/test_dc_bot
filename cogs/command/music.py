import discord
from discord import voice_client
from discord.ext import commands
from discord.ext.commands.core import command
import youtube_dl
from youtube_dl.YoutubeDL import YoutubeDL
from core.cog_class import Cog_basic

class Music(Cog_basic):

    musicCmdGroup = discord.SlashCommandGroup(name="music", description="Command about music.")

    @musicCmdGroup.command(name="join", description="Let bot join your voice channel.")
    async def join(self, ctx:discord.ApplicationContext): 
        if ctx.author.voice is None:
            await ctx.respond("You must join a voice channel!", ephemeral=True)
            return

        if ctx.voice_client is None:
            bvc = await ctx.author.voice.channel.connect()
            await ctx.respond("Join voice channel!", ephemeral=True)
            print(bvc.channel)
            print(bvc.client.voice_clients)
        
        # voice_channel = ctx.author.voice.channel
        # if vc is None:
        #     await voice_channel.connect()
        #     await ctx.respond("Join voice channel!")

    # @musicCmdGroup.command(name="leave", description="Let bot leave your voice channel.")
    # async def leave(self, ctx:discord.ApplicationContext): 
    #     vc = ctx.voice_client
    #     await vc.disconnect()
    #     await ctx.send("Leave voice channel!")

    # @commands.command()
    # async def play(self, ctx, url): 
    #     vc = ctx.voice_client
    #     vc.stop()
    #     FFFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    #     YDL_OPTIONS = {'format':"bestaudio"}

    #     with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
    #         info = ydl.extract_info(url, download=False)
    #         url2 = info['formats'][0]['url']
    #         source = await discord.FFmpegOpusAudio.from_probe(url2, **FFFMPEG_OPTIONS)
    #         vc.play(source)
    #         await ctx.send("Play!")

    # @commands.command()
    # async def pause(self, ctx):
    #     vc = ctx.voice_client
    #     await vc.pause()
    #     await ctx.send("Pause!")

    # @commands.command() 
    # async def resume(self, ctx):
    #     vc = ctx.voice_client
    #     await vc.resume()
    #     await ctx.send("Resume!")

def setup(bot: discord.Bot):
    bot.add_cog(Music(bot))