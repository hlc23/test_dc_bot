# from json import dump
from pixivpy3 import *

REFRESH_TOKEN = "Dv72iY_Mv2vqfcAhSB98x9K_0W85PYOy7h3t9PLe_Aw"

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
