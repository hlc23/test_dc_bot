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
                await msg.reply(choice(safe_load(f)))
            return

def setup(bot: commands.Bot):
    bot.add_cog(Respond(bot))
