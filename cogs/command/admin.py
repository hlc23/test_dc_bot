import discord
from core.cog_class import Cog_basic
from discord.ext import commands

class Admin(Cog_basic):

    @commands.Command
    async def say(self, ctx:commands.Context, channel:discord.TextChannel, msg):
        guild = self.bot.get_guild(self.config["HLCT_guild"])
        guild :discord.Guild
        admin = guild.get_role(self.config["admin_role"])
        if admin not in ctx.author.roles:
            return
        await ctx.message.delete()
        await channel.send(msg)



def setup(bot: commands.Bot):
    bot.add_cog(Admin(bot))