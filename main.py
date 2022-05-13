import discord
import logging
import os
import keep_alive
import json
import _asyncio
from lib.pixiv import recommended
from lib.basic import del_file
import os

# 設定日誌
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# change config
def change_config(key, value):
    print(f"change config: set {key} to {value}")
    with open("./data/config.json",mode="r",encoding="utf-8") as config_file:
        config_data = json.load(config_file)
    config_data[key] = value
    with open("./data/config.json",mode="w",encoding="utf-8") as config_file:
        json.dump(config_data,config_file,indent=4,ensure_ascii=False)


async def delete_message(message:discord.Message, reason:str = "*訊息遭刪除*", reply:bool = True):
    if reply:
        if reason != "":
            await message.reply(content=reason)
        await message.delete()
        return
    else:
        if reason != "":
            await message.channel.send(content=reason)
        await message.delete()
        return


with open("./data/config.json",mode="r",encoding="utf-8") as config_file:
    config = json.load(config_file)

prefix = config["prefix"]


intent = discord.Intents.all()

bot = discord.Client(intents=intent)

@bot.event
async def on_ready():
    print("="*15)
    print(f"login as {bot.user}")
    print("="*15)

@bot.event
async def on_message(message):
    
    if message.author == bot.user:
        return

    guild = bot.get_guild(967615452341739621)

    #say
    if message.content.startswith(f"{prefix}say"):
        if guild.get_role(969962769854128240) not in message.author.roles:
            await message.reply(content=f"{message.author.mention} You can't use this command!")
            await message.delete()
            return
        channel = message.channel_mentions[0]
        if channel.type != discord.ChannelType.text:
            await message.reply(content=f"The channel must be an text channel and the bot must can send message to.")
            return
        content = message.content.replace(f"{prefix}say <#{message.raw_channel_mentions[0]}>","")
        await channel.send(content)

    #help
    if message.content == f"{prefix}help":
        with open("./data/help.txt", mode="r", encoding="utf-8") as help_file:
            help_data = help_file.read()
        await message.reply(help_data)
    
    #hello
    if message.content == f"{prefix}hello":
        if message.author.nick is None:
            mention = message.author.mention
            await message.reply(f"Hi {mention}")
        else:
            mention = message.author.mention
            await message.reply(f"Hi {mention}")

    # ping
    if message.content == f"{prefix}ping":
        await message.reply(f"delay {round(bot.latency*1000)} ms")

    # add role
    if message.content.startswith(f"{prefix}add_role"):
        content = message.content.split(" ")
        if content[0] != f"{prefix}add_role":
            return
        if guild.get_role(969962769854128240) not in message.author.roles:
            await delete_message(message,reason=f"{message.author}你沒有權限使用此指令")
            return
        try:
            await message.mentions[0].add_roles(message.role_mentions[0])
            await delete_message(message,reason=f"{message.mentions[0]} 已成功獲得身分組 ")
            return
        except:
            await delete_message(message,reason="錯誤")
            return

    # me
    if message.content == f"{prefix}me":
        user = message.author
        everyone_role = guild.get_role(967615452341739621)
        for item in user.roles:
            if item == everyone_role:
                continue
            user_role += f"    Name: {item.name}, Id: {item.id}\n"
        await message.reply(f"User: {user}\nDisplay name: {user.display_name}\nActivity: {user.activity}\nRoles:\n{user_role}")

    #pixiv
    if message.content.startswith(f"{prefix}pixiv"):
        if message.content == f"{prefix}pixiv":
            await message.reply(content=f"{prefix}pixiv [數量]")
            return
        text = message.content.split(" ")
        if len(text) != 2:
            await delete_message(message,"指令錯誤")
            return
        try:
            n = int(text[1])
        except:
            await delete_message(message,"引數錯誤")
        if n > 25 or n < 1:
            await delete_message(message,"數量需介於1~25")
            return

        files = os.listdir("./data/image")
        for file in files:
            del_file(path=f"./data/image/{file}")
        recommended(path="./data/image",n=n)
        for image in os.listdir("./data/image/"):
            await message.reply(file=discord.File(f"./data/image/{image}"))
        return
 

# member join
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(967703102436290580)
    await channel.send(f"{member} entered!")

# member leave
@bot.event
async def on_member_leave(member):
    channel = bot.get_channel(967703102436290580)
    await channel.send(f"{member} leaved!")

keep_alive.keep_alive()
bot.run(os.getenv('token'))
