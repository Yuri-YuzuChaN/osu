import os
import aiohttp
import hoshino
from hoshino import Service, util
from hoshino.typing import MessageSegment, NoticeSession, CQEvent

from .osusql import mysql
from .api import get_api, osuapi
from .osu_draw import draw_info, draw_score
from .osu_file import get_user_icon, get_user_header

osupath = os.path.dirname(__file__)
osuhelp = f'{osupath}/OsuFile/osu_help.png'

sv_help = '''
[info]查询自己
[info :num]查询自己在某模式的信息
[info user]查询某位玩家
[info user :num]查询某位玩家在某模式的信息
[bind user]绑定
[unbind]解绑
[mode num]更改查询的默认模式
[update osuid user]更改绑定的用户名
[update icon]更新头像
[recent]查询自己在最近游玩的成绩
[recent :num]查询自己在最近游玩某模式的成绩
[recent user]查询某位玩家在最近游玩的成绩
[recent user :num]查询某位玩家在最近游玩某模式的成绩
[score mapid]查询自己在该地图的成绩
[score mapid :num]查询自己在该地图某模式的成绩
[score user mapid]查询某位玩家在该地图的成绩
[score user mapid :num]查询某位玩家在该地图某模式的成绩

num ： 0 std, 1 taiko, 2 ctb, 3 mania
'''.strip()
sv = Service('osu', enable_on_default=True, visible=True, help_ = sv_help)
key = get_api()
mod = { '0' : 'Std', '1' : 'Taiko', '2' : 'Ctb', '3' : 'Mania'}
osu_api = 'https://osu.ppy.sh/api/'

#输入玩家信息
@sv.on_prefix('info')
async def info(bot, ev:CQEvent):
    qqid = ev.user_id
    uid = ev.message.extract_plain_text().strip()
    sql = f'select osuid,osumod from userinfo where qqid = {qqid}'
    if not uid:
        result = mysql(sql)
        if result:
            for i in result:
                osuid = i[0]
                osumod = i[1]
        else:
            await bot.finish(ev, '该账号尚未绑定，请输入 bind 用户名 绑定账号')
    elif ':' in uid:
        if uid[:-2]:
            osuid = uid[:-2].strip()
            osumod = uid[-1:].strip()
        else:
            result = mysql(sql)
            if result:
                for i in result:
                    osuid = i[0]
                osumod = uid[-1:].strip()
            else:
                await bot.finish(ev, '该账号尚未绑定，请输入 bind 用户名 绑定账号')
    else:
        osuid = uid
        osumod = 0

    msg = await draw_info(osuid, osumod)
    if 'API' in msg:
        await bot.send(ev, msg)
    elif msg:
        await bot.send(ev, msg)
    else:
        await bot.send(ev, '未知错误')

@sv.on_prefix('recent')
async def recent(bot, ev:CQEvent):
    qqid = ev.user_id
    msg = ev.message.extract_plain_text()
    sql = f'select osuname,osumod from userinfo where qqid = {qqid}'
    if not msg:
        result = mysql(sql)
        if result:
            for i in result:
                osuid = i[0]
                osumod = i[1]
        else:
            await bot.finish(ev, '该账号尚未绑定，请输入 bind 用户名 绑定账号')
    elif ':' in msg:
        if msg[:-2]:
            osuid = msg[:-2].strip()
            osumod = msg[-1:].strip()
        else:
            result = mysql(sql)
            if result:
                for i in result:
                    osuid = i[0]
                osumod = msg[-1:].strip()
            else:
                await bot.finish(ev, '该账号尚未绑定，请输入 bind 用户名 绑定账号')
    else:
        osuid = msg
        osumod = 0
    url = f'{osu_api}get_user_recent?k={key}&u={osuid}&m={osumod}'
    msg_ = await draw_score(url, osuid, osumod)
    if msg_:
        if 'API' in msg_:
            await bot.send(ev, msg_)
        else:
            await bot.send(ev, msg_)
    else:
        mid = mod[f'{osumod}']
        msg_ = f'该玩家最近在 {mid} 模式中未有游玩记录！'
        await bot.send(ev, msg_)
        
@sv.on_prefix('score')
async def score(bot, ev:CQEvent):
    qqid = ev.user_id
    msg = ev.message.extract_plain_text().strip().split(' ')
    if '' in msg:
        msg.remove('')
    sql = f'select osuid,osumod,osuname from userinfo where qqid = {qqid}'
    if not msg:
        await bot.finish(ev, '请输入正确的地图ID！')
    if ':' in msg:
        l_num = len(msg) - 2
        if l_num != 0:
            if msg[l_num].isdigit():
                mapid = msg[l_num]
                osuid = ' '.join(msg[:l_num])
                osumod = msg[l_num + 1][-1:]
            else:
                await bot.finish(ev, '请输入正确的地图ID！')
        elif msg[l_num].isdigit():
            mapid = msg[l_num]
            osumod = msg[l_num + 1][-1:]
            result = mysql(sql)
            if result:
                for i in result:
                    osuid = i[2]
            else:
                await bot.finish(ev, '该账号尚未绑定，请输入 bind 用户名 绑定账号')
        else:
            await bot.finish(ev, '请输入正确的地图ID！')
    else:
        l_num = len(msg) - 1
        if l_num != 0:
            if msg[l_num].isdigit():
                mapid = msg[l_num]
                osuid = ' '.join(msg[:l_num])
                osumod = 0
            else:
                await bot.finish(ev, '请输入正确的地图ID！')
        elif msg[l_num].isdigit():
            mapid = msg[l_num]
            result = mysql(sql)
            if result:
                for i in result:
                    osuid = i[2]
                    osumod = i[1]
            else:
                await bot.finish(ev, '该账号尚未绑定，请输入 bind 用户名 绑定账号')
        else:
            await bot.finish(ev, '请输入正确的地图ID！')

    url = f'{osu_api}get_scores?k={key}&b={mapid}&u={osuid}&m={osumod}'
    msg_ = await draw_score(url, osuid, osumod, mapid)
    if msg_:
        if 'API' in msg_:
            await bot.send(ev, msg_)
        else:
            await bot.send(ev, msg_)
    else:
        msg_ = '您在该图未有游玩记录！'
        await bot.send(ev, msg_)
        
@sv.on_prefix('bind')
async def bind(bot, ev:CQEvent):
    qqid = ev.user_id
    uid = ev.message.extract_plain_text()
    if not uid:
        await bot.finish(ev, '请输入您的 osuid')
    sql = f'select * from userinfo where qqid = {qqid}'
    result = mysql(sql)
    if result:
        await bot.finish(ev, '您已绑定，如需要解绑请输入unbind，改绑请输入update osuid 用户名')
    url = f'{osu_api}get_user?k={key}&u={uid}'
    info = await osuapi(url)
    if 'API' in info:
        msg = info
    elif not info:
        msg = '未查询到该用户！'
    else:
        for i in info:
            osuid = i['user_id']
            osuname = i['username']
            sql = f'insert into userinfo values (NULL, {qqid}, {osuid}, "{osuname}", 0)'
            result = mysql(sql)
            if result:
                msg = f'用户 {osuname} 已成功绑定QQ {qqid}'
            else:
                msg = '绑定失败！'
    await bot.send(ev, msg)

@sv.on_prefix('unbind')
async def unbind(bot, ev:CQEvent):
    qqid = ev.user_id
    sel_sql = f'select * from userinfo where qqid = {qqid}'
    sel_result = mysql(sel_sql)
    if sel_result: 
        del_sql = f'delete from userinfo where qqid = {qqid}'
        del_result = mysql(del_sql)
        if del_result:
            await bot.send(ev, '解绑成功！')
        else:
            await bot.send(ev, '数据库错误')
    else:
        await bot.send(ev, '该用户尚未绑定，无需解绑')

@sv.on_prefix('update')
async def update(bot, ev:CQEvent):
    qqid = ev.user_id
    num = ev.message.extract_plain_text().strip().split(' ')
    if '' in num:
        num.remove('')
    sql = f'select * from userinfo where qqid = {qqid}'
    result = mysql(sql)
    osuid = ''
    if not result:
        msg = '该账号尚未绑定，请输入 bind 用户名 绑定账号'
    elif not num:
        msg = '请输入需要更新内容的参数！'
    elif num[0] == 'icon':
        select_id = f'select osuid from userinfo where qqid = {qqid}'
        result = mysql(select_id)
        if result:
            for i in result:
                osuid = i[0]
            get_user_icon(osuid)
            get_user_header(osuid)
            msg = '头像更新完成'
        else:
            msg = '该用户未绑定，无法更新头像！'
    elif num[0] == 'osuid':
        try:
            osuid = num[1]
        except:
            msg = '请输入更改的用户名！'
        info = await select_info(osuid)
        if info:
            for i in info:
                osunum = i['user_id']
                osuname = i['username']
            update_id = f'update userinfo set osuid = {osunum}, osuname = "{osuname}" where qqid = {qqid}'
            result = mysql(update_id)
            if result:
                msg = f'已将QQ {qqid} 绑定的osu用户名更改为 {osuname}'
            else:
                msg = '数据库错误'
        else:
            msg = '未查询到该用户，无法更改用户名！'
    else:
        msg = '参数错误，请输入正确的参数！'
    await bot.send(ev, msg)

@sv.on_prefix('mode')
async def mode(bot, ev:CQEvent):
    qqid = ev.user_id
    num = ev.message.extract_plain_text()
    try:
        num = int(num)
    except:
        await bot.finish(ev, '请输入正确的模式 0-3')
    sql = f'select * from userinfo where qqid = {qqid}'
    result = mysql(sql)
    if not result:
        msg = '该账号尚未绑定，请输入 bind 用户名 绑定账号'
    elif not num:
        msg = '请输入正确的模式 0-3'
    elif num == 0 or num == 1 or num == 2 or num == 3:
        mid = mod[f'{num}']
        sql = f'update userinfo set osumod = {num} where qqid = {qqid}'
        result = mysql(sql)
        if result:
            msg = f'已将默认模式更改为 {mid}'
        else:
            msg = '数据库错误'
    else:
        msg = '请输入正确的模式 0-3'
    await bot.send(ev, msg)

@sv.on_fullmatch('osuhelp')
async def help(bot, ev:CQEvent):
    img = MessageSegment.image(f'file:///{os.path.abspath(osuhelp)}')
    await bot.send(ev, img)

async def select_info(osuid):
    url = f'{osu_api}get_user?k={key}&u={osuid}&m=0'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as req:
                info = req.json()
    except:
        msg = 'User API请求失败，请联系管理员'
        return msg
    if info:
        return info
    else:
        return False
