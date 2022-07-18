from core.cog_class import Cog_basic
from discord.ext import commands
import discord
import discord
import datetime

class Msg_logger(Cog_basic):

    @discord.Cog.listener()
    async def on_message_edit(self, before:discord.Message, after:discord.Message):
        log_channel = self.bot.get_channel(self.config["log_channel"])
        if before.channel != log_channel:
            embed=discord.Embed(title=before.channel, url=after.jump_url, color=0x0000ff)
            embed.set_thumbnail(url=before.author.display_avatar.url)
            embed.set_author(name=before.author.name)
            embed.add_field(name="Type", value="Edit", inline=True)
            embed.add_field(name="Channel", value=before.channel.mention, inline=True)
            embed.add_field(name="Before", value=before.content, inline=False)
            # Before attachments
            if len(before.attachments) != 0:
                for attachment in before.attachments:
                    embed.add_field(name="附件:", value=attachment, inline=False)
            embed.add_field(name="After", value=after.content, inline=False)
            # After attachments
            if len(after.attachments) != 0:
                for attachment in after.attachments:
                    embed.add_field(name="附件:", value=attachment, inline=False)
            embed.add_field(name="ID", value=after.id)
            tzone = datetime.timezone(datetime.timedelta(hours=8))
            now = datetime.datetime.now(tz=tzone)
            embed.set_footer(text=now)
            await log_channel.send(embed=embed)

    @discord.Cog.listener()
    async def on_raw_message_delete(self, payload:discord.RawMessageDeleteEvent):
        log_channel = self.bot.get_channel(self.config["log_channel"])
        if payload.cached_message.channel != log_channel:
            embed=discord.Embed(title=payload.cached_message.channel, url=payload.cached_message.jump_url, color=0xff0000)
            embed.set_thumbnail(url=payload.cached_message.author.display_avatar._url)
            embed.set_author(name=payload.cached_message.author.name)
            embed.add_field(name="Type", value="Delete", inline=True)
            embed.add_field(name="Channel", value=payload.cached_message.channel.mention, inline=True)
            if payload.cached_message.content != "":
                embed.add_field(name="Content:", value=payload.cached_message.content, inline=False)
            if len(payload.cached_message.attachments) != 0:
                for attachment in payload.cached_message.attachments:
                    embed.add_field(name="附件:", value=attachment.url, inline=False)
            embed.add_field(name="ID", value=payload.cached_message.id)
            tzone = datetime.timezone(datetime.timedelta(hours=8))
            now = datetime.datetime.now(tz=tzone)
            embed.set_footer(text=now)
            await log_channel.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Msg_logger(bot))
