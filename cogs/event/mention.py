import discord
from core.cog_class import Cog_basic
from discord.ext import commands

class Mention(Cog_basic):

    @commands.Cog.listener()
    async def on_message(self, msg:discord.Message):
        log_channel = self.bot.get_channel(self.config["log_channel"])
        mention_channel = self.bot.get_channel(self.config["mention_channel"])
        guild = self.bot.get_guild(self.config["HLCT_guild"])
        if msg.author == guild.owner:
            return
        if msg.channel != (log_channel or mention_channel):
            for admin in self.config["admins"]:
                admin = self.bot.get_user(admin)
                if admin in msg.mentions:
                    embed=discord.Embed(title=msg.channel, url=msg.jump_url, color=0x00ff00)
                    embed.set_thumbnail(url=msg.author.avatar_url)
                    embed.set_author(name=msg.author.name)
                    embed.add_field(name="Content", value=msg.content)
                    embed.description = guild.owner.mention
                    await self.bot.get_channel(self.config["mention_channel"]).send(embed=embed)



def setup(bot: commands.Bot):
    bot.add_cog(Mention(bot))
