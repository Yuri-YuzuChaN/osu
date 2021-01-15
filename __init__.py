import os
import aiohttp
import hoshino
from hoshino import Service, util
from hoshino.typing import MessageSegment, NoticeSession, CQEvent
import requests
import json

from .osusql import mysql
from .api import get_api, osuapi
from .osu_draw import draw_info, draw_score, best_pfm
from .osu_file import get_user_icon, get_user_header

osupath = os.path.dirname(__file__)
osuhelp = f'{osupath}/OsuFile/osu_help.png'

sv_help = '''
[osuhelp] 查看指令
'''.strip()
sv = Service('osu', enable_on_default=True, visible=True, help_ = sv_help)
key = get_api()
mod = { '0' : 'Std', '1' : 'Taiko', '2' : 'Ctb', '3' : 'Mania'}
osu_api = 'https://osu.ppy.sh/api/'

#输出玩家信息
@sv.on_prefix('info')
async def info(bot, ev:CQEvent):
    qqid = ev.user_id
    msg = ev.message.extract_plain_text().strip().split(' ')
    if '' in msg:
        msg.remove('')
    sql = f'select osuid,osumod from userinfo where qqid = {qqid}'
    result = mysql(sql)
    list_len = len(msg)
    if not msg:
        if result:
            for i in result:
                osuid = i[0]
                osumod = i[1]
        else:
            await bot.finish(ev, '该账号尚未绑定，请输入 bind 用户名 绑定账号')
    elif list_len == 1:
        if ':' in msg[-1]:
            if result:
                for i in result:
                    osuid = i[0]
                osumod = msg[-1][1]
            else:
                await bot.finish(ev, '该账号尚未绑定，请输入 bind 用户名 绑定账号')
        else:
            osuid = msg[0]
            osumod = 0
    elif list_len >= 2:
        if ':' in msg[-1]:
            osuid = ' '.join(msg[:list_len-1])
            osumod = msg[-1][1]
        else:
            osuid = ' '.join(msg[:list_len-1])
            osumod = 0
    else:
        await bot.finish(ev, '请输入正确的参数')

    msg = await draw_info(osuid, osumod)
    if msg:
        if 'API' in msg:
            await bot.send(ev, msg)
        elif msg:
            await bot.send(ev, msg)
    else:
        await bot.send(ev, '未知错误')

@sv.on_prefix('recent')
async def recent(bot, ev:CQEvent):
    qqid = ev.user_id
    msg = ev.message.extract_plain_text().strip().split(' ')
    if '' in msg:
        msg.remove('')
    sql = f'select osuname,osumod from userinfo where qqid = {qqid}'
    result = mysql(sql)
    list_len = len(msg)
    if not msg:
        if result:
            for i in result:
                osuid = i[0]
                osumod = i[1]
        else:
            await bot.finish(ev, '该账号尚未绑定，请输入 bind 用户名 绑定账号')
    elif list_len == 1:
        if ':' in msg[-1]:
            if result:
                for i in result:
                    osuid = i[0]
                osumod = msg[-1][1]
            else:
                await bot.finish(ev, '该账号尚未绑定，请输入 bind 用户名 绑定账号')
        else:
            osuid = msg[0]
            osumod = 0
    elif list_len >= 2:
        if ':' in msg[-1]:
            osuid = ' '.join(msg[:list_len-1])
            osumod = msg[-1][1]
        else:
            osuid = ' '.join(msg[:list_len-1])
            osumod = 0
    else:
        await bot.finish(ev, '请输入正确的参数')

    url = f'{osu_api}get_user_recent?k={key}&u={osuid}&m={osumod}'
    info = await draw_score(url, osuid, osumod)
    if info:
        if 'API' in info:
            await bot.send(ev, info)
        else:
            await bot.send(ev, info)
    else:
        mid = mod[f'{osumod}']
        if not msg:
            id = '您'
        else:
            id = osuid
        info = f'{id} 最近在 {mid} 模式中未有游玩记录！'
        await bot.send(ev, info)
        
@sv.on_prefix('score')
async def score(bot, ev:CQEvent):
    qqid = ev.user_id
    num = ev.message.extract_plain_text().strip().split(' ')
    if '' in num:
        num.remove('')
    sql = f'select osuid,osumod,osuname from userinfo where qqid = {qqid}'
    result = mysql(sql)
    list_len = len(num)
    if list_len == 1:
        if num[0].isdigit() and result:
            for i in result:
                osuid = i[0]
                osumod = i[1]
            mapid = num[0]
        elif not result:
            await bot.finish(ev, '该账号尚未绑定，请输入 bind 用户名 绑定账号')
        else:
            await bot.finish(ev, '请输入正确的地图ID！')
    elif list_len == 2:
        if ':' in num[-1] and num[0].isdigit() and result:
            for i in result:
                osuid = i[0]
            mapid = num[0]
            osumod = num[-1][1]
        elif num[-1].isdigit():
            osuid = num[0]
            mapid = num[-1]
            osumod = 0
        elif not result:
            await bot.finish(ev, '该账号尚未绑定，请输入 bind 用户名 绑定账号')
        else:
            await bot.finish(ev, '请输入正确的地图ID！')
    elif list_len >=3:
        if ':' in num[-1] and num[-2].isdigit():
            osuid = ' '.join(num[:list_len-2])
            mapid = num[-2]
            osumod = num[-1][1]
        else:
            await bot.finish(ev, '请输入正确的地图ID！')
    else:
        await bot.finish(ev, '请输入正确的地图ID！')

    url = f'{osu_api}get_scores?k={key}&b={mapid}&u={osuid}&m={osumod}'
    msg = await draw_score(url, osuid, osumod, mapid=mapid)
    if msg:
        if 'API' in msg:
            await bot.send(ev, msg)
        else:
            await bot.send(ev, msg)
    else:
        if not num:
            id = '您'
        else:
            id = osuid
        num = f'{id} 在该图未有游玩记录！'
        await bot.send(ev, msg)
        
@sv.on_prefix('bp')
async def best(bot, ev:CQEvent):
    qqid = ev.user_id
    num = ev.message.extract_plain_text().strip().split(' ')
    osumod = 0
    if '' in num:
        num.remove('')
    if len(num) != 1:
        if num[0] == '1' or num[0] == '2' or num[0] == '3':
            osumod = num[0]
            del num[0]
    bpnum = ''
    sql = f'select osuname from userinfo where qqid = {qqid}'
    result = mysql(sql)
    list_len = len(num)
    if num[0] == 'list':
        if list_len == 2:
            if '-' in num[-1] and result:
                li = num[-1].split('-')
                min = int(li[0])
                max = int(li[1])
                range_limit = max - min +1
                if min >= max:
                    await bot.finish(ev, '请输入正确的bp范围')
                elif range_limit > 10:
                    await bot.finish(ev, '只允许查询10个bp成绩')
                elif max > 10:
                    limit = 100
                elif max <= 10:
                    limit = 10
                for i in result:
                    osuid = i[0]
            elif not result:
                await bot.finish(ev, '该账号尚未绑定，请输入 bind 用户名 绑定账号')
        elif list_len > 2:
            if '-' in num[-1]:
                li = num[-1].split('-')
                min = int(li[0])
                max = int(li[1])
                range_limit = max - min +1
                if min >= max:
                    await bot.finish(ev, '请输入正确的bp范围')
                elif range_limit > 10:
                    await bot.finish(ev, '只允许查询10个bp成绩')
                elif max > 10:
                    limit = 100
                elif max <= 10:
                    limit = 10
                osuid = ' '.join(num[1:-1])
            else:
                await bot.finish(ev, '请输入正确的参数')
        else:
            await bot.finish(ev, '请输入正确的参数')
    elif list_len == 1:
        if num[0].isdigit() and result:
            if int(num[0]) <= 0 or int(num[0]) > 100:
                await bot.finish(ev, '只允许查询bp 1-100 的成绩')
            for i in result:
                osuid = i[0]
            bpnum = int(num[0])
            limit = 100 if bpnum > 10 else 10
        elif not result:
            await bot.finish(ev, '该账号尚未绑定，请输入 bind 用户名 绑定账号')
        else:
            await bot.finish(ev, '请输入正确的参数')
    elif list_len >= 2:
        if num[-1].isdigit():
            if int(num[-1]) <= 0 or int(num[-1]) > 100:
                await bot.finish(ev, '只允许查询bp 1-100 的成绩')
            osuid = ' '.join(num[:list_len-1])
            bpnum = int(num[-1])
            limit = 100 if bpnum > 10 else 10
        else:
            await bot.finish(ev, '请输入正确的参数')

    url = f'{osu_api}get_user_best?k={key}&u={osuid}&m={osumod}&limit={limit}'
    if bpnum:
        info = await draw_score(url, osuid, osumod, bpnum=bpnum)
    else:
        mid = mod[f'{osumod}']
        info = await best_pfm(url, osuid, mid, min, max)
    if info:
        if 'API' in info:
            await bot.send(ev, info)
        else:
            await bot.send(ev, info)
    else:
        info = '未知错误'
        await bot.send(ev, info)
        
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
        url = f'{osu_api}get_user?k={key}&u={osuid}&m=0'
        info = await osuapi(url)
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
    sql = f'select * from userinfo where qqid = {qqid}'
    result = mysql(sql)
    if not result:
        msg = '该账号尚未绑定，请输入 bind 用户名 绑定账号'
    elif not num:
        msg = '请输入正确的模式 0-3'
    elif num == '0' or num == '1' or num == '2' or num == '3':
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
