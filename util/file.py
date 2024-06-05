import os
import json

def del_file(path:str):
    try:
        os.remove(path)
        return True
    except:
        return False
    
def read_json(path:str):
    with open(path, mode="r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def load_config():
    return read_json("./data/config.json")

def get_cogs():
    return read_json("./data/cogs.json")["cogs"]