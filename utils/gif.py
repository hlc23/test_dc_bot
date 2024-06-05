import requests
import json

apikey = "N0PMCLWQG914" 
lmt = 1

def gifsearch(keyword:str):
    search_term = keyword
    r = requests.get(f"https://g.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}&locale=zh_TW&contentfilter=high")
    if r.status_code == 200:
        gif = json.loads(r.content)
        return gif["results"][0]["media"][0]["gif"]["url"]
    return None
