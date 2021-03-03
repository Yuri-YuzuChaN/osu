import aiohttp, os, re, zipfile, aiohttp
from PIL import Image

osupath = os.path.dirname(__file__)
osufile = f'{osupath}/OsuFile/'
mapfile = f'{osufile}map/'
usericon = f'{osufile}user_icon/'

async def Download(mapid):
    # 判断是否存在该文件
    mapid = str(mapid)
    for file in os.listdir(mapfile):
        if mapid in file:
            if os.path.exists(f'{mapfile}{file}'):
                return f'{mapfile}{file}'
        continue
    else:
        url = f'https://txy1.sayobot.cn/beatmaps/download/novideo/{mapid}'
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, allow_redirects = False) as re:
                    sayo = re.headers['Location']
        except:
            print('Request Failed or Timeout')
            return
        filename = await get_osz(sayo, mapid)
        filepath = mapfile + filename
        # 解压下载的osz文件
        myzip = zipfile.ZipFile(filepath)
        mystr = myzip.filename.split(".")
        myzip.extractall(mystr[0])
        myzip.close()
        end = ['mp3','wav','mp4','avi','mov','ogg','osb','flv']
        # 删除其余不需要的文件
        for root, dirs, files in os.walk(filepath[:-4], topdown=False):
            for name in files:
                for i in end:
                    if name.endswith(i):
                        os.remove(os.path.join(root, name))

        # 删除下载osz文件
        os.remove(filepath)
        return filepath[:-4]
        
async def get_osz(sayo, mapid):
    try:
        print('Start Downloading Map')
        async with aiohttp.ClientSession() as session:
            async with session.get(sayo) as req:
                filename = f'{mapid}.osz'
                chunk = await req.read()
                open(f'{mapfile}{filename}', 'wb').write(chunk)
        print('Map Download Complete')
        return filename
    except:
        print('Map Download Failed')
        return

# 获取version文件
def get_file(path, mapid, version):
    for file in os.listdir(path):
        if '.osu' in file:
            with open(f'{path}/{file}', 'r', encoding='utf-8') as f:
                text = f.read()
            result = re.finditer(r'BeatmapID:(.+)', text)
            try:
                for i in result:
                    rmapid = i.groups()[0]
                if mapid == rmapid:
                    filepath = f'{path}/{file}'
                    return filepath
            except:
                continue
    else:
        for file in os.listdir(path):
            if version in file:
                filepath = f'{path}/{file}'
                return filepath

# 获取version BG
def get_picture(path):
    p =[]
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    result = re.finditer(r'\d,\d,\"(.+?)\"', text)
    for i in result:
        return i.groups()[0]

#获取头像
async def get_user_icon(uid, update = False):
    uid = str(uid)
    if not update:
        for file in os.listdir(usericon):
            if uid in file:
                if 'h' not in file:
                    return f'{usericon}{file}'
            continue
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://a.ppy.sh/{uid}') as req:
            path = f'{usericon}{uid}.png'
            chunk = await req.read()
            open(path, 'wb').write(chunk)
    icon = Image.new('RGBA', (256, 256), '#FFFFFFFF')
    w_icon = Image.open(path).convert('RGBA').resize((256,256))
    icon.alpha_composite(w_icon)
    icon.save(path)
    return path
    
async def get_user_header(uid, update = False):
    uid = str(uid)
    if not update:
        for file in os.listdir(usericon):
            if uid in file:
                if 'h' in file:
                    return f'{usericon}{file}'
            continue
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://osu.ppy.sh/users/{uid}') as req:
            html = await req.text()
    result = re.finditer(r'assets\.ppy\.sh\\/user(\S*)', html)
    if result:
        for i in result:
            imgurl = i.group().split('"')[0]
            break
        else:
            imgurl = 'osu.ppy.sh/images/headers/profile-covers/c1.jpg'
        url = f'https://{imgurl}'.replace('\\', '')
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as req:
                html = req.text
                path = f'{usericon}{uid}_h.png'
                chunk = await req.read()
                open(path, 'wb').write(chunk)
        return path
    else:
        return False
