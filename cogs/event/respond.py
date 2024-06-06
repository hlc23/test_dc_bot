from core.cog_class import Cog_basic

import discord
from discord.ext import commands
from random import choice
from yaml import safe_load

class Respond(Cog_basic):

    @discord.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return
        if msg.content == "艸":
            with open("./data/fuck_text.yaml", "r", encoding="utf-8") as f:
                text = choice(safe_load(f))
            
            await msg.channel.send(text)
            return

        if msg.author.guild_permissions.administrator:
            if msg.content.startswith(".") and msg.content[1:4] == "say":     
                await msg.delete()
                if len(msg.content) > 5:
                    await msg.channel.send(msg.content[5:])
                if len(msg.attachments) != 0:
                    for attachments in msg.attachments:
                        await msg.channel.send(attachments.url)
                return
        return


def setup(bot: commands.Bot):
    bot.add_cog(Respond(bot))
