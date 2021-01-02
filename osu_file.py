import requests
from contextlib import closing
import hoshino
import os
import re
import json
import zipfile
from PIL import Image

osupath = os.path.dirname(__file__)
osufile = f'{osupath}/OsuFile/'
mapfile = f'{osufile}/map/'
usericon = f'{osufile}/user_icon/'

def Download(mapid):
    filename = f'{mapid}.osz'
    filepath = f'{mapfile}{filename}'
    # 判断是否存在该文件
    if os.path.exists(filepath[:-4]):
        return filepath[:-4]
    else:
        sayo = requests.get(f'https://txy1.sayobot.cn/beatmaps/download/full/{mapid}', allow_redirects = False)
        dl = sayo.headers['location']

        osz = requests.get(dl, stream = True)
        # 开始下载osz文件
        with closing(osz) as response:
            chunk_size = 1024
            with open(filepath, 'wb') as f :
                for data in response.iter_content(chunk_size = chunk_size):
                    f.write(data)
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
    result = re.finditer(r'"(\S*?jpg|\S*?JPG|\S*?jpeg|\S*?JPEG|\S*?png|\S*?PNG)"', text)
    for i in result:
        return i.group().strip('"')

#获取头像
def get_user_icon(uid):
    res = requests.get(f'https://a.ppy.sh/{uid}')
    path = f'{usericon}{uid}.png'
    open(path, 'wb').write(res.content)
    icon = Image.new('RGBA', (256, 256), '#FFFFFFFF')
    w_icon = Image.open(path).convert('RGBA').resize((256,256))
    icon.alpha_composite(w_icon)
    icon.save(path)
    return path
