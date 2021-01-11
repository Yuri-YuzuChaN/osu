import aiohttp

def get_api():
    api = ''
    return api

async def osuapi(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as re:
                info = await re.json()
        return info
    except:
        msg = 'API请求失败，请联系管理员'
        return msg
