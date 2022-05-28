from core.cog_class import Cog_basic
from discord.ext import commands
import discord
import discord
import datetime

class Logger(Cog_basic):

    @commands.Cog.listener()
    async def on_message(self, msg:commands.Context):
        log_channel = self.bot.get_channel(self.config["log_channel"])
        if msg.channel != log_channel:
            color = discord.Colour.random()
            embed=discord.Embed(title=msg.channel, url=msg.jump_url, color=color)
            embed.set_thumbnail(url=msg.author.avatar_url)
            embed.set_author(name=msg.author.name)
            embed.add_field(name="Type", value="Sent", inline=False)
            embed.add_field(name="Content:", value=msg.content, inline=False)
            if len(msg.attachments) != 0:
                for attachment in msg.attachments:
                    embed.add_field(name="附件:", value=attachment, inline=False)
            tzone = datetime.timezone(datetime.timedelta(hours=8))
            now = datetime.datetime.now(tz=tzone)
            embed.set_footer(text=now)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before:discord.Message, after:discord.Message):
        log_channel = self.bot.get_channel(self.config["log_channel"])
        if before.channel != log_channel:
            color = discord.Colour.random()
            embed=discord.Embed(title=before.channel.mention, url=before.jump_url, description="Edit", color=color)
            embed.set_author(name=before.author.name)
            embed.set_thumbnail(url=before.author.avatar_url)
            embed.add_field(name="Before", value=before.content, inline=False)
            if len(before.attachments) != 0:
                for attachment in before.attachments:
                    embed.add_field(name="附件:", value=attachment, inline=False)
            embed.add_field(name="After", value=after.content, inline=False)
            if len(after.attachments) != 0:
                for attachment in after.attachments:
                    embed.add_field(name="附件:", value=attachment, inline=False)
            embed.add_field(name="頻道", value="test", inline=False)
            await log_channel.send(embed=embed)
        

def setup(bot: commands.Bot):
    bot.add_cog(Logger(bot))