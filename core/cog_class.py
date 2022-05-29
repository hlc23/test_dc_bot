import discord
from discord.ext import commands
import json
from typing import List

class Cog_basic(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        with open("./data/config.json", mode="r", encoding="utf-8") as config_file:
            self.config = json.load(config_file)
        self.guild = self.bot.get_guild(self.config["HLCT_guild"])
        self.guild: discord.Guild

    def is_role(self, ctx:commands.Context, role_id:int):
        '''
        @commands.Command
        @commands.check(is_role)
        async def ping(self, ctx):
            pass
        '''
        return self.guild.get_role(role_id) in ctx.author.roles
    
    def is_roles(self, ctx:commands.Context, role_ids:List[int]):
        for role_id in role_ids:
            role = self.guild.get_role(role_id)
            if role in ctx.author.roles:
                return True
        return False
