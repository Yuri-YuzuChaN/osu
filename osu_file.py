import aiohttp
import requests
from contextlib import closing
import hoshino
import os
import re
import json
import zipfile
import aiohttp
from PIL import Image
from urllib import parse

osupath = os.path.dirname(__file__)
osufile = f'{osupath}/OsuFile/'
mapfile = f'{osufile}/map/'
usericon = f'{osufile}/user_icon/'

async def Download(mapid):
    # 判断是否存在该文件
    mapid = str(mapid)
    for file in os.listdir(mapfile):
        if mapid in file:
            if os.path.exists(f'{mapfile}{file}'):
                return f'{mapfile}{file}'
        continue
    else:
        url = f'https://txy1.sayobot.cn/beatmaps/download/full/{mapid}'
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, allow_redirects = False) as re:
                    sayo = re.headers['Location']
        except:
            print('请求失败或超时')
            return
        filename = await get_osz(sayo)
        filepath = mapfile + filename
        # 解压下载的osz文件
        myzip = zipfile.ZipFile(filepath)
        mystr = myzip.filename.split(".")
        myzip.extractall(mystr[0])
        myzip.close()
        end = ['mp3','wav','mp4','avi','mov','ogg','osb']
        # 删除其余不需要的文件
        for root, dirs, files in os.walk(filepath[:-4], topdown=False):
            for name in files:
                for i in end:
                    if name.endswith(i):
                        os.remove(os.path.join(root, name))

        # 删除下载osz文件
        os.remove(filepath)
        return filepath[:-4]
        
async def get_osz(sayo):
    try:
        print('开始下载')
        async with aiohttp.ClientSession() as session:
            async with session.get(sayo) as req:
                title = req.headers['Content-Disposition'].split('"')
                filename = parse.unquote(title[1])
                chunk = await req.read()
                open(f'{mapfile}{filename}', 'wb').write(chunk)
        return filename
    except:
        print('地图下载失败')
        return

# 获取version文件
def get_file(path, version):
    for file in os.listdir(path):
        if version in file:
            filepath = f'{path}/{file}'
            return filepath

# 获取version BG
def get_picture(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    result = re.finditer(r'\"(.+)\"', text)
    for i in result:
        return i.group().strip('"')

#获取头像
def get_user_icon(uid, update = False):
    if not update:
        for file in os.listdir(usericon):
            if uid in file:
                if 'h' not in file:
                    return f'{usericon}{file}'
            continue
    res = requests.get(f'https://a.ppy.sh/{uid}')
    path = f'{usericon}{uid}.png'
    open(path, 'wb').write(res.content)
    icon = Image.new('RGBA', (256, 256), '#FFFFFFFF')
    w_icon = Image.open(path).convert('RGBA').resize((256,256))
    icon.alpha_composite(w_icon)
    icon.save(path)
    return path
    
def get_user_header(uid, update = False):
    if not update:
        for file in os.listdir(usericon):
            if uid in file:
                if 'h' in file:
                    return f'{usericon}{file}'
            continue
    res = requests.get(f'https://osu.ppy.sh/users/{uid}')
    html = res.text
    result = re.finditer(r'assets\.ppy\.sh\\/user(\S*)"', html)
    if result:
        for i in result:
            imgurl = i.group().split('"')[0]
        url = f'https://{imgurl}'.replace('\\', '')
        img = requests.get(url)
        path = f'{usericon}{uid}_h.png'
        open(path, 'wb').write(img.content)
        return path
    else:
        return False
