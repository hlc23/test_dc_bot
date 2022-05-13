from pixivpy3 import *

REFRESH_TOKEN = "Dv72iY_Mv2vqfcAhSB98x9K_0W85PYOy7h3t9PLe_Aw"

def recommended(path:str="./", n:int=0):
    if n>25:
        return
    api = AppPixivAPI()
    api.auth(refresh_token=REFRESH_TOKEN)

    json_result = api.illust_recommended()
    for t in range(n):
        api.download(json_result.illusts[t].image_urls.medium,path=path,fname=f"image{t+1}.png")
