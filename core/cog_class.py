import discord
from discord.ext import commands
import json

class Cog_basic(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        with open("./data/config.json", mode="r", encoding="utf-8") as config_file:
            self.config = json.load(config_file)
        self.guild = self.bot.get_guild(self.config["HLCT_guild"])
        self.guild: discord.Guild


    async def delete_message(self, ctx:commands.Context, reason:str = "***這裡曾有一則訊息，但現在不在了***"):
        await ctx.message.delete()
        if reason is None or reason == "":
            return
        await ctx.send(reason)
