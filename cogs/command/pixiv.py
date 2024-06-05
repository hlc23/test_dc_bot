from util.pixiv import *
from core.cog_class import Cog_basic
from discord.ext import commands
import discord
import os

class Pixiv(Cog_basic):
    
    @discord.slash_command(name="pixiv")
    async def pixiv(self, ctx:discord.ApplicationContext):
        if ctx.channel != self.bot.get_channel(974633423178190909):
            await ctx.respond("你不能在這裡使用此指令")
            return

        await ctx.respond("您的指令正在處理中", ephemeral=True)

        PIXIV_TOKEN = os.getenv("PIXIV_API_KEY")
        api = AppPixivAPI()
        api.auth(refresh_token=PIXIV_TOKEN)
        json_result = api.illust_recommended()
        if not os.path.exists("data/pixiv/"):
            os.makedirs("data/pixiv/")
        for illust in json_result.illusts:
            api.download(illust.image_urls.medium, path="data/pixiv/")
            embed = discord.Embed(title=illust.title, colour=discord.Colour.from_rgb(r=0, g=155, b=255), description=f"https://www.pixiv.net/artworks/{illust.id}")
            embed.set_footer(text=illust.user.name)
            file = os.listdir("./data/pixiv/")
            await self.bot.get_channel(974633423178190909).send(embed=embed, file=discord.File(f'./data/pixiv/{file[0]}') )
            os.remove(f'./data/pixiv/{file[0]}')

        return

def setup(bot: commands.Bot):
    bot.add_cog(Pixiv(bot))
