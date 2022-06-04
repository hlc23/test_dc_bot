from lib.gif import gifsearch
from discord.ext import commands
from core.cog_class import Cog_basic
from discord import Embed

class Gif(Cog_basic):

    @commands.Command
    async def tenor(self, ctx:commands.Context, keyword:str):
        embed = Embed(title=keyword)
        embed.set_image(url=gifsearch(keyword))
        embed.set_author(name=ctx.author)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.display_name)
        await ctx.send(embed=embed)


def setup(bot:commands.Bot):
    bot.add_cog(Gif(bot))
