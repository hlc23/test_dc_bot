import discord
import logging
import os
import keep_alive
import json
import _asyncio

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
        content = message.content.replace(f"{prefix}say","")
        if content == "":
            await message.reply(content="???")
        else:
            await message.reply(content)

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
        if message.content == f"{prefix}add_role":
            await message.reply(content = f"{prefix}add_role [target id] [role id]")
            return
        if guild.get_role(969962769854128240) not in message.author.roles:
            await message.reply(content = f"{message.author.mention} You can't use this command!")
            await message.delete()
            return
        elif message.channel != guild.get_channel(973520841625174026):
            await message.reply(content = f"{message.author.mention} You can't use this command here!")
            await message.delete()
            return
        else:
            try:
                text = message.content.split(" ")
                try:
                    target_id = text[1]
                except IndexError:
                    await message.reply(content= "Missing argument 'target', it should be the id of the target.")
                    await message.delete()
                    return
                try:
                    role = text[2]
                except IndexError:
                    await message.reply(content= "Missing argument 'role', it should be the id of the role you want.")
                    await message.delete()
                    return
            except:
                await message.reply(content="Unknow Error.")
                await message.delete()
                return
            target = guild.get_member(int(target_id))
            if target is None:
                await message.reply(content= "Didn't find the user with the id.")
                return
            else:
                
                role = guild.get_role(int(role))
                if role is None:
                    await message.reply(content= "Didn't find the role with the id.")
                    return
                elif role in target.roles:
                    await message.reply(content= "This member already has this role")
                    return
                else:
                    try:
                        await target.add_roles(role)
                        await message.reply(content = "Success.")
                    except:
                        await message.reply(content = "Unknow Error.")

    # me
    if message.content == f"{prefix}me":
        user = message.author
        everyone_role = guild.get_role(967615452341739621)
        for item in user.roles:
            if item == everyone_role:
                continue
            user_role += f"    Name: {item.name}, Id: {item.id}\n"
        await message.reply(f"User: {user}\nDisplay name: {user.display_name}\nActivity: {user.activity}\nRoles:\n{user_role}")

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
