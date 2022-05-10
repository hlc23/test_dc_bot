import discord
import logging
import os
import keep_alive
import sys
import json

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

class Bot(discord.Client):
    # init
    def __init__(self,intent):
        super().__init__()
        self.intent = discord.Intents.all()
        with open("./data/config.json",mode="r",encoding="utf-8") as config_file:
            config = json.load(config_file)
        self.prefix = config['prefix']

    # 登入bot提示訊息
    async def on_ready(self):
        print('')
        print(f"{bot.user} has online.")
        print("="*15)

    # 訊息判斷
    async def on_message(self,message):
        # 避免被自己的訊息觸發
        if message.author == self.user:
            return

        # 回覆 help
        if message.content.startswith(f"{self.prefix}help"):
            print(f"{message.author} used 'help'")
            with open("./data/help.txt", mode="r", encoding="utf-8") as help_file:
                help_data = help_file.read()
            await message.reply(help_data)
          
        # 回覆 hello
        if message.content.startswith(f"{self.prefix}hello"):
            print(f"{message.author} used 'hello'")
            await message.reply("Hello")
          
        # 回覆 hi
        if message.content.startswith(f"{self.prefix}hi"):
            print(f"{message.author} used 'hi'")
            await message.reply("Hi")
          
        
        # change prefix 
        if message.content.startswith(f"{self.prefix}prefix"):
            print(f"{message.author} used 'prefix'")
            new_prefix = message.content.split(" ")[1]
            await message.reply(f"change prefix from '{self.prefix}' to '{new_prefix}'.")
            change_config("prefix",new_prefix)
            print(f"prefix set '{new_prefix}'")
            self.prefix = new_prefix

        # 重新載入
        if message.content == f"{self.prefix}reload":
            print(f"{message.author} used 'reload'")
            await message.reply("reloading...")
            os.system('python3 reload.py')
            sys.exit()
  
        
intent = discord.Intents.all()
bot = Bot(intent)
keep_alive.keep_alive()
bot.run(os.getenv('token'))
