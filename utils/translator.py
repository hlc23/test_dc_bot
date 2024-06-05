import requests

def translations(Lang: str, text:str):
    """
    Send https requests to RapidAPI to use microsoft translator.

    Args:
        Lang (str): Target Language
        Text (str): Text want translations

    Returns:
        str
    """
    url = "https://microsoft-translator-text.p.rapidapi.com/translate"

    querystring = {"to[0]":Lang,"api-version":"3.0","profanityAction":"NoAction","textType":"plain"}

    payload = [{"Text": text}]
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "a82a7ebe55msh131e6262eafaebcp121544jsn3674bc5eea81",
        "X-RapidAPI-Host": "microsoft-translator-text.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

    data:str = eval(response.text)[0]["translations"][0]["text"]

    return data