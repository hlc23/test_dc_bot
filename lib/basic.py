import os

def del_file(path:str):
    try:
        os.remove(path)
        return True
    except:
        return False