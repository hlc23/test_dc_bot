import discord
from core.cog_class import Cog_basic
from discord.ext import commands

class Member_logger(Cog_basic):

    # Normal leave guild
    @discord.Cog.listener()
    async def on_member_remove(self, member:discord.Member):
        guild = self.bot.get_guild(self.config["HLCT_guild"])
        normal_role = guild.get_role(self.config["normal_role"])
        if normal_role in member.roles:
            log_channel = self.bot.get_channel(self.config["log_channel"])
            embed=discord.Embed(title="Member", color=0xbeff00)
            embed.set_author(name=member.name, icon_url=member.display_avatar.url)
            embed.add_field(name="Type", value="Leave", inline=True)
            embed.add_field(name="Top role", value=member.top_role, inline=False)
            await log_channel.send(embed=embed)
            border_channel = self.bot.get_channel(self.config["border_channel"])
            embed=discord.Embed(title="成員離開", description=member.mention)
            embed.set_thumbnail(url=member.display_avatar.url)
            await border_channel.send(embed=embed)


def setup(bot: discord.Bot):
    bot.add_cog(Member_logger(bot))
