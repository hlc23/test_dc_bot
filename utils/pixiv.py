# from json import dump
from pixivpy3 import *
import dotenv
import os

REFRESH_TOKEN = os.getenv("PIXIV_REFRESH_TOKEN")

def recommended():
    api = AppPixivAPI()
    api.auth(refresh_token=REFRESH_TOKEN)

    json_result = api.illust_recommended()
    return json_result


def search(key:str, n:int):
    api = AppPixivAPI()
    api.auth(refresh_token=REFRESH_TOKEN)


    json_result = api.search_illust(key)
    n = n
    for illust in json_result.illusts:
        if n <= 0:
            break
        api.download(illust.image_urls.medium, path="./data/image/")
        n -= 1
