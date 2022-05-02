import discord
import logging
import os
import keep_alive
import sys

# 設定日誌
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class Bot(discord.Client):
    # init
    def __init__(self):
        super().__init__()
        self.prefix = "!"

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

        # 重新載入
        if message.content == f"{self.prefix}reload":
            print(f"{message.author} used 'reload'")
            os.system('python3 reload.py')
            sys.exit()

      
bot = Bot()
keep_alive.keep_alive()
bot.run(os.getenv('token'))
