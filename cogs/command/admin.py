import discord
from core.cog_class import Cog_basic
from discord.ext import commands

class Admin(Cog_basic):


    @discord.command(name="join", description="Let someone in.")
    async def join(self, ctx:discord.ApplicationContext, member:discord.Member):
        print(ctx.author.guild_permissions.administrator)
        if ctx.author.guild_permissions.administrator is False:
            embed = discord.Embed(title="您無使用此指令的權限", colour=discord.Colour.red())
            await ctx.respond(embed=embed, ephemeral=True)
            return
        self.guild = self.bot.get_guild(self.config["HLCT_guild"])
        normal_role = self.guild.get_role(969962597061373994)
        border_channel = self.bot.get_channel(self.config["border_channel"])
        await member.add_roles(normal_role)
        embed=discord.Embed(title="成員加入", description=member.mention)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=member.name)
        await border_channel.send(embed=embed)
        await ctx.respond(f"{member.mention} 已成功加入", ephemeral=True)

def setup(bot: discord.Bot):
    bot.add_cog(Admin(bot))
