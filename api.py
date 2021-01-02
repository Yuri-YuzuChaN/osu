from hoshino import util
import requests
import json

def get_api():
    jsonpath = './hoshino/modules/osu/'
    with open(f'{jsonpath}config.json', encoding='utf-8') as d:
        jsondata = json.load(d)
        api = jsondata['apikey']
        return api