from pixivpy3 import *

REFRESH_TOKEN = "Dv72iY_Mv2vqfcAhSB98x9K_0W85PYOy7h3t9PLe_Aw"

def recommended(path:str="./", n:int=0):
    if n>20:
        return
    api = AppPixivAPI()
    api.auth(refresh_token=REFRESH_TOKEN)

    json_result = api.illust_recommended()
    for t in range(n):
        api.download(json_result.illusts[t].image_urls.medium,path=path,fname=f"image{t+1}.png")


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



