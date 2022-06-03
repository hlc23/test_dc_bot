import discord
from discord.ext import commands
import json
from dotenv import load_dotenv
import os
from keep_alive import keep_alive

def load_config():
    global config
    with open("./data/config.json", mode="r", encoding="utf-8") as config_file:
        config = json.load(config_file)
    

load_dotenv()
load_config()

bot = commands.Bot(command_prefix=config["prefix"], intents = discord.Intents.all())


@bot.event
async def on_ready():
    print("="*15)
    print(f"login as {bot.user}")
    print("="*15)

@bot.command()
async def reload(ctx:commands.Context):
    guild = bot.get_guild(config["HLCT_guild"])
    guild :discord.Guild
    admin = guild.get_role(config["admin_role"])
    if admin not in ctx.author.roles:
        return
    load_config()
    for cog in config["cogs"]:
        try:
            bot.reload_extension(f"cogs.{cog}")
        except:
            bot.load_extension(f"cogs.{cog}")
    await ctx.send("reload complete")

@bot.event
async def on_error(event, *args, **kwargs):
    load_config()
    for cog in config["cogs"]:
        try:
            bot.reload_extension(f"cogs.{cog}")
        except:
            bot.load_extension(f"cogs.{cog}")
    rc = bot.get_channel(981463832906063912)
    rc.send("reloaded")


for cog in config["cogs"]:
    bot.load_extension(f"cogs.{cog}")

# keep_alive()
try:
    bot.run(os.getenv("token"))
except:
    os.system("kill 1")
