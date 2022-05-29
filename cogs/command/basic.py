from core.cog_class import Cog_basic
from discord.ext import commands

class Basic(Cog_basic):

    @commands.Command
    async def ping(self, ctx):
        await ctx.send(f"延遲:{round(self.bot.latency*1000)} ms")

def setup(bot: commands.Bot):
    bot.add_cog(Basic(bot))
