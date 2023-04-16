import discord
from discord.ext import commands
from dotenv import load_dotenv
import json
import os
# from keep_alive import keep_alive

def load_config():
    with open("./data/config.json", mode="r", encoding="utf-8") as config_file:
        global config
        config = json.load(config_file)
def get_cogs():
    with open("./data/cogs.json", mode="r", encoding="utf-8") as cogs_file:
        global cogs
        cogs = json.load(cogs_file)["cogs"]

load_dotenv()
load_config()
get_cogs()

bot = commands.Bot(debug_guilds=[967615452341739621], intents=discord.Intents.all(), command_prefix="!")

@bot.event
async def on_ready():
    print("="*15)
    print(f"{bot.user} v1.2 is ready and online!")
    print("="*15)
    return

@bot.slash_command(name = "reload", description = "Reload cog")
@commands.has_permissions(administrator=True)
async def reload(ctx:discord.ApplicationContext):
    try:
        load_config()
        get_cogs()
        for cog in cogs:
            try:
                bot.reload_extension(f"cogs.{cog}")
            except:
                bot.load_extension(f"cogs.{cog}")
    except:
        await ctx.respond("Error", ephemeral=True)
    else:
        await ctx.respond("Reload complete", ephemeral=True)
    return

for cog in cogs:
    bot.load_extension(f"cogs.{cog}")

# print(bot.cogs.items())


# keep_alive()
# bot.run(os.getenv("TOKEN"))
try:
    bot.run(os.getenv('TOKEN'))
except:
    os.system("kill 1")
