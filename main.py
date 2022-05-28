from discord.ext import commands
import json
from dotenv import load_dotenv
import os

def load_config():
    global config
    with open("./data/config.json", mode="r", encoding="utf-8") as config_file:
        config = json.load(config_file)
    

load_dotenv()
load_config()
bot = commands.Bot(command_prefix=config["prefix"])


@bot.event
async def on_ready():
    print("="*15)
    print(f"login as {bot.user}")
    print("="*15)

@bot.command()
async def reload(ctx):
    load_config()
    for cog in config["cogs"]:
        try:
            bot.reload_extension(f"cogs.{cog}")
        except:
            bot.load_extension(f"cogs.{cog}")
    await ctx.send("reload complete")



for cog in config["cogs"]:
    bot.load_extension(f"cogs.{cog}")

bot.run(os.getenv("token"))
