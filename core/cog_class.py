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

