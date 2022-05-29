from lib.pixiv import *
from core.cog_class import Cog_basic
from discord.ext import commands
import discord
import os
from lib.basic import *

class Pixiv(Cog_basic):
    
    @commands.Command
    async def pixiv(self, ctx:commands.Context, num:int):
        if ctx.channel != self.bot.get_channel(974633423178190909):
            await ctx.send("***這裡曾有一則訊息，但現在不在了***")
            await ctx.message.delete()
            return
        if num < 1 or num >20:
            await ctx.send("***這裡曾有一則訊息，但現在不在了***")
            await ctx.message.delete()
            return
        files = os.listdir("./data/image")
        for file in files:
            del_file(path=f"./data/image/{file}")
        recommended(path="./data/image",n=num)
        for image in os.listdir("./data/image/"):
            await ctx.channel.send(file=discord.File(f"./data/image/{image}"))
        await ctx.message.delete()
        return

def setup(bot: commands.Bot):
    bot.add_cog(Pixiv(bot))