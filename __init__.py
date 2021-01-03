import os
import hoshino
from hoshino import Service, util
from hoshino.typing import MessageSegment, NoticeSession, CQEvent
import nonebot
from nonebot import on_command
import requests
import json

from .osusql import mysql
from .api import get_api
from .osu_draw import draw_info, draw_score
from .osu_file import get_user_icon

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
[pr/recent]查询自己在最近游玩的成绩
[pr/recent :num]查询自己在最近游玩某模式的成绩
[pr/recent user]查询某位玩家在最近游玩的成绩
[pr/recent user :num]查询某位玩家在最近游玩某模式的成绩
[score mapid]查询自己在该地图的成绩
[score mapid :num]查询自己在该地图某模式的成绩
[score user mapid]查询某位玩家在该地图的成绩
[score user mapid :num]查询某位玩家在该地图某模式的成绩

num ： 0 std, 1 taiko, 2 ctb, 3 mania
'''.strip()
sv = Service('osu', enable_on_default=True, visible=True, help_ = sv_help)

key = get_api()
mod = { '0' : 'Std', '1' : 'Taiko', '2' : 'Ctb', '3' : 'Mania'}

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

    osuinfo = requests.get(f'https://osu.ppy.sh/api/get_user?k={key}&u={osuid}&m={osumod}')
    img = draw_info(osuinfo, osumod)
    if img:
        await bot.send(ev, MessageSegment.image(img))
    else:
        await bot.finish(ev, '未查询到该用户！')

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

    recentinfo = requests.get(f'https://osu.ppy.sh/api/get_user_recent?k={key}&u={osuid}&m={osumod}')
    img = draw_score(recentinfo, osuid, osumod)
    if img: 
        await bot.send(ev, MessageSegment.image(img)) 
    else:
        mid = mod[f'{osumod}']
        await bot.send(ev, f'该玩家最近在 {mid} 模式中未有游玩记录！')
        
@sv.on_prefix('score')
async def score(bot, ev:CQEvent):
    qqid = ev.user_id
    msg = ev.message.extract_plain_text()
    msg_ = msg.strip().split(' ')
    if '' in msg_:
        msg_.remove('')
    sql = f'select osuid,osumod,osuname from userinfo where qqid = {qqid}'
    if msg:
        if ':' in msg:
            l_num = len(msg_) - 2
            if l_num != 0:
                if msg_[l_num].isdigit():
                    mapid = msg_[l_num]
                    osuid = ' '.join(msg_[:l_num])
                    osumod = msg_[l_num + 1][-1:]
                else:
                    await bot.finish(ev, '请输入正确的地图ID！')
            elif msg_[l_num].isdigit():
                mapid = msg_[l_num]
                osumod = msg_[l_num + 1][-1:]
                result = mysql(sql)
                if result:
                    for i in result:
                        osuid = i[2]
                else:
                    await bot.finish(ev, '该账号尚未绑定，请输入 bind 用户名 绑定账号')
            else:
                await bot.finish(ev, '请输入正确的地图ID！')
        else:
            l_num = len(msg_) - 1
            if l_num != 0:
                if msg_[l_num].isdigit():
                    mapid = msg_[l_num]
                    osuid = ' '.join(msg_[:l_num])
                    osumod = 0
                else:
                    await bot.finish(ev, '请输入正确的地图ID！')
            else:
                if msg_[l_num].isdigit():
                    mapid = msg_[l_num]
                    result = mysql(sql)
                    if result:
                        for i in result:
                            osuid = i[2]
                            osumod = i[1]
                    else:
                        await bot.finish(ev, '该账号尚未绑定，请输入 bind 用户名 绑定账号')
                else:
                    await bot.finish(ev, '请输入正确的地图ID！')
    else:
        await bot.finish(ev, '请输入正确的地图ID！')
    recentinfo = requests.get(f'https://osu.ppy.sh/api/get_scores?k={key}&b={mapid}&u={osuid}&m={osumod}')
    img = draw_score(recentinfo, osuid, osumod, mapid)
    if img:
        await bot.send(ev, MessageSegment.image(img))
    else:
        await bot.send(ev, f'您在该图未有游玩记录！')
        
@sv.on_prefix('bind')
async def bind(bot, ev:CQEvent):
    qqid = ev.user_id
    uid = ev.message.extract_plain_text()
    jsondata = select_info(uid)
    if jsondata:
        if uid:
            sql = f'select * from userinfo where qqid = {qqid}'
            result = mysql(sql)
            if not result:
                for i in jsondata:
                    osuid = i['user_id']
                    osuname = i['username']
                try:
                    sql = f'insert into userinfo values (0,{qqid},{osuid},"{osuname}",0)'
                    msg = mysql(sql)
                    if msg:
                        await bot.send(ev, f'用户 {osuname} 已成功绑定QQ {qqid}')
                    else:
                        await bot.send(ev, '绑定失败！')
                except:
                    await bot.send(ev, '未知错误，绑定失败！')
            else :
                await bot.send(ev, '您已绑定，如需要解绑请输入unbind，改绑请输入bind osuid 用户名')
        else:
            await bot.send(ev, '请输入您的 osu id')
    else:
        await bot.send(ev, '未查询到该用户！')

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
    msg = ev.message.extract_plain_text().strip()
    msg_ = msg.strip().split(' ')
    if '' in msg_:
        msg_.remove('')
    sql = f'select * from userinfo where qqid = {qqid}'
    result = mysql(sql)
    if result:
        if msg:
            if msg_[0] == 'icon':
                select_id = f'select osuid from userinfo where qqid = {qqid}'
                result = mysql(select_id)
                if result:
                    for i in result:
                        osuid = i[0]
                    get_user_icon(osuid)
                    await bot.send(ev, '头像更新完成')
                else:
                    await bot.send(ev, '该用户未绑定，无法更新头像！')
            elif msg_[0] == 'osuid':
                osuid = msg_[1]
                jsondata = select_info(osuid)
                if jsondata:
                    for i in jsondata:
                        osunum = i['user_id']
                        osuname = i['username']
                    update_id = f'update userinfo set osuid = {osunum}, osuname = "{osuname}" where qqid = {qqid}'
                    result = mysql(update_id)
                    if result:
                        await bot.send(ev, f'已将QQ {qqid} 绑定的osu用户名更改为 {osuname}')
                    else:
                        await bot.send(ev, '数据库错误')
                else:
                    await bot.send(ev, '未查询到该用户，无法更改用户名！')
            else:
                await bot.send(ev, '参数错误，请输入正确的参数！')
        else:
            await bot.send(ev, '请输入需要更新内容的参数！')
    else:
        await bot.send(ev, '该账号尚未绑定，请输入 bind 用户名 绑定账号')

@sv.on_prefix('mode')
async def mode(bot, ev:CQEvent):
    qqid = ev.user_id
    num = ev.message.extract_plain_text()
    sql = f'select * from userinfo where qqid = {qqid}'
    result = mysql(sql)
    if result:
        if num:
            if num != 0 or 1 or 2 or 3:
                mid = mod[f'{num}']
                sql = f'update userinfo set osumod = {num} where qqid = {qqid}'
                result = mysql(sql)
                if result:
                    await bot.send(ev, f'已将默认模式更改为 {mid}')
                else:
                    await bot.send(ev, '数据库错误')
            else:
                await bot.send(ev, '请输入正确的模式 0-3')
        else:
            await bot.send(ev, '请输入正确的模式 0-3')
    else:
        await bot.send(ev, '该账号尚未绑定，请输入 bind 用户名 绑定账号')

@sv.on_fullmatch('osuhelp')
async def help(bot, ev:CQEvent):
    await bot.send(ev, MessageSegment.image(f'file:///{os.path.abspath(osuhelp)}'))

# 未绑定查询
def select_info(osuid):
    url = f'https://osu.ppy.sh/api/get_user?k={key}&u={osuid}&m=0'
    result = requests.get(url)
    jsondata = json.loads(result.text)
    if jsondata:
        return jsondata 
    else:
        return False
