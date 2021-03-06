from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from hoshino.typing import MessageSegment
import os
import time
from datetime import datetime, timedelta

from .osu_file import Download, get_file, get_picture, get_user_icon, get_user_header
from .api import *
from .osu_pp import *
from .mods import *

osupath = os.path.dirname(__file__)
osufile = f'{osupath}/OsuFile/'
imagePath = f'{osupath}/work/'

outputPath = f'{osufile}output/'
usericonPath = f'{osufile}user_icon/'

Exo2_Medium = os.path.join(imagePath, 'fonts', 'Exo2-Medium.otf')
Exo2_Bold = os.path.join(imagePath, 'fonts', 'Exo2-Bold.otf')
Torus_Regular = os.path.join(imagePath, 'fonts', 'Torus Regular.otf')
Torus_SemiBold = os.path.join(imagePath, 'fonts', 'Torus SemiBold.otf')

key = get_api()
approved_num = {'-2' : 'Graveyard', '-1' : 'WIP', '0' : 'Pending', '1' : 'Ranked', '2' : 'Approved', '3' : 'Qualified', '4' : 'Loved'}
mod = { '0' : 'std', '1' : 'taiko', '2' : 'ctb', '3' : 'mania'}
api = 'https://osu.ppy.sh/api/'

class picture:
    def __init__(self, L, T, Path):
        self.L = L
        self.T = T
        self.path = Path
        
class datatext:
    #L=X轴，T=Y轴，size=字体大小，fontpath=字体文件，
    def __init__(self, L, T, size, text, path, anchor = 'lt'):
        self.L = L
        self.T = T
        self.text = str(text)
        self.path = path
        self.font = ImageFont.truetype(self.path, size)
        self.anchor = anchor

def write_text(image, font, text='text', pos=(0, 0), color=(255, 255, 255, 255), anchor='lt'):
    rgba_image = image.convert('RGBA')
    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)
    image_draw.text(pos, text, font=font, fill=color, anchor=anchor)
    return Image.alpha_composite(rgba_image, text_overlay)

def draw_text(image, class_text: datatext, color=(255, 255, 255, 255)):
    font = class_text.font
    text = class_text.text
    anchor = class_text.anchor
    return write_text(image, font, text, (class_text.L, class_text.T), color, anchor)

def draw_fillet(img, radii):
    # 画圆（用于分离4个角）
    circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建一个黑色背景的画布
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 画白色圆形
    # 原图
    img = img.convert("RGBA")
    w, h = img.size
    # 画4个角（将整圆分离为4个部分）
    alpha = Image.new('L', img.size, 255)
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
    alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
    alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角

    img.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见
    return img

#裁切图片
def crop_bg(path, size):
    bg = Image.open(path).convert('RGBA')
    #获取长宽
    bg_width = bg.size[0]
    bg_height = bg.size[1]
    #固定长宽
    if size == 'BG':
        fix_height = 1088
        fix_width = 1950
    elif size == 'S':
        fix_height = 296
        fix_width = 436
    elif size == 'H':
        fix_height = 325
        fix_width = 1200
    #固定比例
    fix_scale = fix_height / fix_width
    #图片比例
    bg_scale = bg_height / bg_width
    #当图片比例大于固定比例
    if bg_scale > fix_scale:
        #长比例
        scale_width = fix_width / bg_width
        #等比例缩放
        width = int(scale_width * bg_width)
        height = int(scale_width * bg_height)
        sf = bg.resize((width, height))
        #计算上下裁切
        crop_height = (height - fix_height) / 2
        x1, y1, x2, y2 = 0, crop_height, width, height - crop_height
        #裁切保存
        crop_img = sf.crop((x1, y1, x2, y2))
        return crop_img
    #当图片比例小于固定比例
    elif bg_scale < fix_scale:
        #宽比例
        scale_height = fix_height / bg_height
        #等比例缩放
        width = int(scale_height * bg_width)
        height = int(scale_height * bg_height)
        sf = bg.resize((width, height))
        #计算左右裁切
        crop_width = (width - fix_width) / 2
        x1, y1, x2, y2 = crop_width, 0, width - crop_width, height
        #裁切保存
        crop_img = sf.crop((x1, y1, x2, y2))
        return crop_img
    else:
        return path

def stars_diff(stars):
    diff = ''
    if 0 < stars < 2.0:
        diff = 'easy'
    elif 2.0 <= stars < 2.7:
        diff = 'normal'
    elif 2.7 <= stars < 4.0:
        diff = 'hard'
    elif 4.0 <= stars < 5.3:
        diff = 'insane'
    elif 5.3 <= stars < 6.5:
        diff = 'expert'
    elif 6.5 <= stars :
        diff = 'expertplus'
    return diff

def rank_score(rank):
    rankimg = ''
    if rank == 'XH':
        rankimg =  'ranking-XH.png'
    elif rank == 'X':
        rankimg =  'ranking-X.png'
    elif rank == 'SH':
        rankimg =  'ranking-SH.png'
    elif rank == 'S':
        rankimg =  'ranking-S.png'
    elif rank == 'A':
        rankimg =  'ranking-A.png'
    elif rank == 'B':
        rankimg =  'ranking-B.png'
    elif rank == 'C':
        rankimg =  'ranking-C.png'
    elif rank == 'D':
        rankimg =  'ranking-D.png'
    else:
        rankimg =  'ranking-F.png'
    return rankimg

def percent_color(percent):
    red = 255
    green = 255
    if percent > 0.5:
        red = int(255 - 255 * percent)
    else:
        green = int(255 * percent)
    return red, green

def set_mod_list(json, modnum):
    vnum =[]
    for index, v in enumerate(json):
        if v['enabled_mods'] == str(modnum):
            vnum.append(index)
    return vnum

async def draw_info(osuid, osumod):
    url = f'{api}get_user?k={key}&u={osuid}&m={osumod}'
    info = await osuapi(url)
    if 'API' in info:
        msg = info
    elif info:
        try:
            for s in info:
                uid = s['user_id']
                username = s['username']
                c300 = int(s['count300'])
                c100 = int(s['count100'])
                c50 = int(s['count50'])
                pc = int(s['playcount'])
                r_score = int(s['ranked_score'])
                t_score = int(s['total_score'])
                g_ranked = int(s['pp_rank'])
                lv = s['level']
                pp = s['pp_raw']
                acc = round(float(s['accuracy']), 2)
                c_r_ss = s['count_rank_ss']
                c_r_ssh = s['count_rank_ssh']
                c_r_s = s['count_rank_s']
                c_r_sh = s['count_rank_sh']
                c_r_a = s['count_rank_a']
                country = s['country']
                play_time = s['total_seconds_played']
                c_ranked = int(s['pp_country_rank'])

            info_bg = os.path.join(imagePath, 'default-info-v1.png')

            #背景
            bg = picture(1200, 857, info_bg)
            im = Image.new('RGBA', (bg.L, bg.T))
            
            #底图
            header_img = await get_user_header(uid)
            if header_img:
                header_d = crop_bg(header_img, 'H')
                header_gb = header_d.filter(ImageFilter.GaussianBlur(2))
                h_img = ImageEnhance.Brightness(header_gb).enhance(4 / 4.0)
                im.alpha_composite(h_img)

            #背景
            bg_img = Image.open(bg.path).convert('RGBA')
            im.alpha_composite(bg_img)
            
            #头像
            #获取头像
            user_icon = await get_user_icon(uid)
            icon_f = Image.open(user_icon)
            #头像圆角
            icon_s = draw_fillet(icon_f, 50)
            icon_img = icon_s.resize((190, 190))
            im.alpha_composite(icon_img, (40, 55))

            #地区
            area = picture(272, 212, os.path.join(imagePath, 'flags', f'{country}.png'))
            area_img = Image.open(area.path).convert('RGBA').resize((60, 38))
            im.alpha_composite(area_img, (area.L, area.T))

            #模式
            mode = picture(1125, 10, os.path.join(imagePath, 'mode_icon', f'{osumod}.png'))
            mode_img = Image.open(mode.path).convert('RGBA').resize((63, 63))
            im.alpha_composite(mode_img, (mode.L, mode.T))

            #PP+
            ppplus = picture(0, 0, os.path.join(imagePath, 'nopp+info-v1.png'))
            ppplus_img = Image.open(ppplus.path).convert('RGBA')
            im.alpha_composite(ppplus_img)

            #更新时间
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            w_times = datatext(10, 13, 20, f'update:  {times}', Exo2_Medium, anchor='lm')
            im = draw_text(im, w_times)

            #用户名
            w_username = datatext(273, 120, 58, username, Exo2_Bold, anchor='ls')
            im = draw_text(im, w_username)

            #地区排名
            w_c_ranked = datatext(335, 230, 20, '#{}'.format(c_ranked, ','), Exo2_Medium)
            im = draw_text(im, w_c_ranked)

            #世界排名
            w_g_ranked = datatext(42, 375, 36, format(g_ranked, ','), Exo2_Medium)
            im = draw_text(im, w_g_ranked)

            #PP
            w_pp = datatext(248, 375, 36, pp, Exo2_Medium)
            im = draw_text(im, w_pp)

            #等级
            lv_list = lv.split('.')
            w_lv = datatext(1115.5, 365, 30, lv_list[0], Exo2_Medium, anchor='mm')
            im = draw_text(im, w_lv)
            
            #经验百分比
            lv_list[0] = '0'
            lv_num = float('.'.join(lv_list))
            lv_num_p = format(lv_num, '.0%')
            w_lv_p = datatext(1060, 390, 20, lv_num_p, Exo2_Medium, anchor='rm')
            im = draw_text(im, w_lv_p)
            lv_p = Image.new('RGBA', (int(400 * lv_num), 8), '#FF66AE')
            lv_p_img = draw_fillet(lv_p, 4)
            im.alpha_composite(lv_p_img, (662, 370))

            #评级数量
            w_ssh = datatext(81, 525, 28, c_r_ssh, Exo2_Medium, anchor='mm')
            im = draw_text(im, w_ssh)
            w_ss = datatext(191, 525, 28, c_r_ss, Exo2_Medium, anchor='mm')
            im = draw_text(im, w_ss)
            w_sh = datatext(301, 525, 28, c_r_sh, Exo2_Medium, anchor='mm')
            im = draw_text(im, w_sh)
            w_s = datatext(411, 525, 28, c_r_s, Exo2_Medium, anchor='mm')
            im = draw_text(im, w_s)
            w_a = datatext(521, 525, 28, c_r_a, Exo2_Medium, anchor='mm')
            im = draw_text(im, w_a)

            #ranked总分
            w_r_score = datatext(1180, 606, 32, format(r_score, ','), Exo2_Medium, anchor='rm')
            im = draw_text(im, w_r_score)

            #acc
            w_acc = datatext(1180, 646, 32, f'{acc}%', Exo2_Medium, anchor='rm')
            im = draw_text(im, w_acc)

            #游玩次数
            w_pc = datatext(1180, 686, 32, format(pc, ','), Exo2_Medium, anchor='rm')
            im = draw_text(im, w_pc)

            #总分
            w_t_score = datatext(1180, 726, 32, format(t_score, ','), Exo2_Medium, anchor='rm')
            im = draw_text(im, w_t_score)
            
            #命中次数
            t_count = c300 + c100 + c50
            w_count = datatext(1180, 766, 32, format(t_count, ','), Exo2_Medium, anchor='rm')
            im = draw_text(im, w_count)
            
            #游玩时间
            sec = timedelta(seconds = int(play_time))
            d_time = datetime(1, 1, 1, 1) + sec
            t_time = "%dd %dh %dm %ds" % (d_time.day-1, d_time.hour, d_time.minute, d_time.second)
            w_time = datatext(1180, 806, 32, t_time, Exo2_Medium, anchor='rm')
            im = draw_text(im, w_time)

            #完整图
            info_img = f'info_{uid}.png'
            outputImage_path = os.path.join(outputPath, info_img)
            im.save(outputImage_path)
            
            msg = MessageSegment.image(f'file:///{os.path.abspath(outputPath + info_img)}')
        except Exception as e:
            msg = f'制图错误：{e}'
    else:
        msg = '未查询到该用户'
    return msg

async def draw_score(url, username, osumod, mapid=0, bpnum=0, setmod=0):
    map_pp = []
    play_json = await osuapi(url)
    if 'API' in play_json:
        msg = play_json
    elif play_json:
        try:
            #如果不是查询BP，则是recent指令
            if bpnum == 0:
                s = play_json[0]
            #如果查询开mod bp
            elif setmod != 0:
                modlist = set_mod_list(play_json, setmod)
                if not modlist:
                    return '没有在bp上查询到开启该mod的成绩'
                s = play_json[modlist[bpnum - 1]]
            #如果查询bp
            else:
                s = play_json[bpnum - 1]
            #如果有指定第几张图
            if mapid == 0:
                mapid = s['beatmap_id']
            #如果查询bp，返回pp
            for i in ['get_user_best', 'get_scores']:
                if i in url:
                    pp = int(float(s['pp']))
                    break
            else:
                pp = '--'
            
            uid = s['user_id']
            mods_num = int(s['enabled_mods'])
            score = s['score']
            maxcb = int(s['maxcombo'])
            c50 = int(s['count50'])
            c100 = int(s['count100'])
            c300 = int(s['count300'])
            cmiss = int(s['countmiss'])
            ckatu = int(s['countkatu'])
            cgeki = int(s['countgeki'])
            date = s['date']
            rank = s['rank']
            
            url_ = f'{api}get_beatmaps?k={key}&b={mapid}'
            beatmaps_json = await osuapi(url_)
            for i in beatmaps_json:
                bmapid = i['beatmapset_id']
                approved = i['approved']
                total_len = i['total_length']
                artist = i['artist']
                title = i['title']
                creator = i['creator']
                cs = i['diff_size']
                ar = i['diff_approach']
                od = i['diff_overall']
                hp = i['diff_drain']
                bpm = i['bpm']
                version = i['version']
                stars = float(i['difficultyrating'])
                if osumod != 3:
                    map_maxcb = int(i['max_combo'])
            
            # 下载地图并获取地图路径
            dirpath = await Download(bmapid)
            
            # 获取开启的mod
            mods = resolve(mods_num)

            # 获取version地图文件
            ver_file = get_file(dirpath, mapid, version)

            # 计算该地图的pp
            if osumod == 0:
                map_pp = calc_acc_pp(ver_file, mods_num)
            
            # 计算该次游玩的pp
                stars, cs, ar, od, hp, pp, aim_pp, speed_pp, acc_pp, acc = calc_pp(ver_file, mods_num, maxcb, c50, c100, c300, cmiss)
            else:
                a = 0
                while a < 6:
                    map_pp.append('--')
                    a+=1
                stars, cs, ar, od, hp, pp, aim_pp, speed_pp, acc_pp, acc = [stars, cs, ar, od, hp, pp, '--', '--', '--', '--']
                
            #获取BG
            map_bg = get_picture(ver_file)
            map_path = f'{dirpath}/{map_bg}'

            recent_img = os.path.join(imagePath, 'default-score-v2.png')

            #创建新图
            im = Image.new('RGBA', (1950, 1088))

            #将地图BG做背景，加高斯模糊，降低亮度
            bg_b = crop_bg(map_path, 'BG')
            bg_gb = bg_b.filter(ImageFilter.GaussianBlur(4))
            bg_img = ImageEnhance.Brightness(bg_gb).enhance(3 / 4.0)
            im.alpha_composite(bg_img)

            #成绩背景
            recent = picture(0, 0, recent_img)
            recent_bg = Image.open(recent.path).convert('RGBA')
            im.alpha_composite(recent_bg)

            #地图BG
            #裁剪左上BG
            bg_img_s = crop_bg(map_path, 'S')
            #圆角BG
            bg_img_f = draw_fillet(bg_img_s, 22)
            d_bg = picture(26, 34, bg_img_f)
            im.alpha_composite(bg_img_f, (d_bg.L, d_bg.T))

            #rank状态
            if approved != '-2' and approved != '-1' and approved != '0':
                app_num = approved_num[f'{approved}']
                app = picture(415, 16, os.path.join(imagePath, 'icons', f'{app_num}.png'))
                app_img = Image.open(app.path).convert('RGBA').resize((70, 70))
                im.alpha_composite(app_img, (app.L, app.T))

            #版本图片
            mod_id = mod[f'{osumod}']
            diff_img = f'{mod_id}-{stars_diff(stars)}'
            ver = picture(506, 255, os.path.join(imagePath, 'icons', f'{diff_img}.png'))
            ver_img = Image.open(ver.path).convert('RGBA').resize((70, 70))
            im.alpha_composite(ver_img, (ver.L, ver.T))

            #头像
            #获取头像
            user_icon = await get_user_icon(uid)
            icon_f = Image.open(user_icon)
            #头像画圆
            icon_d = draw_fillet(icon_f, 128)
            icon_img = icon_d.resize((80, 80))
            im.alpha_composite(icon_img, (40, 425))

            #mod
            if mods != 'NO':
                de_f = 440
                for sw_mod in mods:
                    mod_d = picture(de_f, 440, os.path.join(imagePath, 'mods', f'{sw_mod}.png'))
                    mod_img = Image.open(mod_d.path).convert('RGBA').resize((200, 60))
                    im.alpha_composite(mod_img, (mod_d.L, mod_d.T))
                    de_f += 160
            
            #评分
            rank_ = picture(913, 874, os.path.join(imagePath, 'ranking', rank_score(rank)))
            rank_img = Image.open(rank_.path).convert('RGBA')
            im.alpha_composite(rank_img, (rank_.L, rank_.T))

            #曲名
            if len(title) > 25:
                title = title[:25] + '...'
            w_title = datatext(500, 55, 50, title, Torus_Regular)
            im = draw_text(im, w_title)

            #作曲
            if len(artist) > 11:
                artist = artist[:11] + '...'
            w_artist = datatext(520, 135, 36, artist, Torus_Regular)
            im = draw_text(im, w_artist)

            #mapper
            if len(creator) > 9:
                creator = creator[:9] + '...'
            w_creator = datatext(795, 135, 36, creator, Torus_Regular)
            im = draw_text(im, w_creator)

            #mapid
            w_mapid = datatext(1005, 135, 36, mapid, Torus_Regular)
            im = draw_text(im, w_mapid)

            #难度
            w_stars = datatext(585, 265, 25, f'Stars:{round(float(stars), 2)}', Torus_Regular)
            im = draw_text(im, w_stars, color=(255, 215, 0, 255))

            #谱面版本
            if len(version) > 10:
                version = version[:10] + '...'
            w_version = datatext(585, 292, 25, version, Torus_Regular)
            im = draw_text(im, w_version)
            
            #BP,时长,MAR,OD,CS,HP
            #谱面时长
            map_len = list(divmod(int(total_len), 60))
            map_len[1] = map_len[1] if map_len[1] >= 10 else f'0{map_len[1]}'
            music_len = f'{map_len[0]}:{map_len[1]}'
            if rank == 'F':
                play_seconds = calc_time(ver_file, c50, c100, c300, cmiss)
                game_len = list(divmod(int(play_seconds / 1000), 60))
                game_len[1] = game_len[1] if game_len[1] >= 10 else f'0{game_len[1]}'
                gaming_len = f'{game_len[0]}:{game_len[1]}'
                play_len = gaming_len
            else:
                play_len = music_len
            w_bpm = datatext(1455, 103, 22, bpm, Torus_Regular)
            im = draw_text(im, w_bpm, color=(255, 215, 0, 255))
            w_time = datatext(1740, 103, 22, f'{play_len} / {music_len}', Torus_Regular)
            im = draw_text(im, w_time, color=(255, 215, 0, 255))
            w_ar = datatext(1455, 194, 22, round(float(ar), 1), Torus_Regular)
            im = draw_text(im, w_ar, color=(255, 215, 0, 255))
            w_od = datatext(1740, 194, 22, round(float(od), 1), Torus_Regular)
            im = draw_text(im, w_od, color=(255, 215, 0, 255))
            w_cs = datatext(1455, 287, 22, round(float(cs), 1), Torus_Regular)
            im = draw_text(im, w_cs, color=(255, 215, 0, 255))
            w_hp = datatext(1740, 287, 22, round(float(hp), 1), Torus_Regular)
            im = draw_text(im, w_hp, color=(255, 215, 0, 255))

            #用户名
            w_username = datatext(145, 430, 36, username, Torus_SemiBold)
            im = draw_text(im, w_username)

            #游玩时间
            sdate = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            newtime = (sdate + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
            w_date = datatext(145, 477, 26, newtime, Torus_Regular)
            im = draw_text(im, w_date)

            #游玩PP
            w_pp = datatext(1900, 450, 50, f'{pp}pp', Torus_Regular, anchor='rt')
            im = draw_text(im, w_pp, color=(255, 106, 178, 255))

            #if fc pp
            if osumod != 0:
                if_pp = '--'
            else:
                if_pp = int(calc_if(ver_file, mods_num, c50, c100, map_maxcb))
            w_if_pp = datatext(105, 540, 26, f'{if_pp}pp', Torus_Regular)
            im = draw_text(im, w_if_pp, color=(255, 106, 178, 255))

            #95-100% pp
            w_95pp = datatext(50, 610, 30, f'{map_pp[0]}pp', Torus_Regular)
            im = draw_text(im, w_95pp, color=(255, 106, 178, 255))
            w_97pp = datatext(190, 610, 30, f'{map_pp[2]}pp', Torus_Regular)
            im = draw_text(im, w_97pp, color=(255, 106, 178, 255))
            w_98pp = datatext(330, 610, 30, f'{map_pp[3]}pp', Torus_Regular)
            im = draw_text(im, w_98pp, color=(255, 106, 178, 255))
            w_99pp = datatext(468, 610, 30, f'{map_pp[4]}pp', Torus_Regular)
            im = draw_text(im, w_99pp, color=(255, 106, 178, 255))
            w_100pp = datatext(607, 610, 30, f'{map_pp[5]}pp', Torus_Regular)
            im = draw_text(im, w_100pp, color=(255, 106, 178, 255))

            #aim,speed,acc pp
            w_aim_pp = datatext(1533, 610, 30, f'{aim_pp}pp', Torus_Regular)
            im = draw_text(im, w_aim_pp, color=(255, 106, 178, 255))
            w_speed_pp = datatext(1673, 610, 30, f'{speed_pp}pp', Torus_Regular)
            im = draw_text(im, w_speed_pp, color=(255, 106, 178, 255))
            w_acc_pp = datatext(1813, 610, 30, f'{acc_pp}pp', Torus_Regular)
            im = draw_text(im, w_acc_pp, color=(255, 106, 178, 255))

            #分数
            w_score = datatext(974, 715, 45, format(int(score), ','), Torus_Regular, anchor='mt')
            im = draw_text(im, w_score)

            # acc
            acc = round(calc_acc(osumod, c50, c100, c300, cmiss, ckatu, cgeki), 2)
            w_acc = datatext(350, 950, 45, f'{acc}%', Torus_Regular, anchor='mm')
            accred , accgreen = percent_color(acc/100)
            im = draw_text(im, w_acc, color=(accred, accgreen, 50, 255))

            # 300,100,50,miss
            if osumod != 0:
                p300 = f'{c300}/{cgeki}'
                p100 = f'{c100}/{ckatu}'
            else:
                p300 = c300
                p100 = c100
            w_c300 = datatext(792, 820, 40, p300, Torus_Regular, anchor='mt')
            im = draw_text(im, w_c300)
            w_c100 = datatext(792, 950, 40, p100, Torus_Regular, anchor='mt')
            im = draw_text(im, w_c100)
            w_c50 = datatext(1156, 820, 40, c50, Torus_Regular, anchor='mt')
            im = draw_text(im, w_c50)
            w_cmiss = datatext(1156, 950, 40, cmiss, Torus_Regular, anchor='mt')
            im = draw_text(im, w_cmiss)

            #combo
            if osumod == 3:
                w_maxcb = datatext(1600, 950, 45, f'{maxcb}x', Torus_Regular, anchor='mm')
                im = draw_text(im, w_maxcb, color=(255, 255, 0, 255))
            else:
                cbred, cbgreen = percent_color(maxcb / map_maxcb)
                w_maxcb = datatext(1590, 950, 45, f'{maxcb}x', Torus_Regular, anchor='rm')
                im = draw_text(im, w_maxcb, color=(cbred, cbgreen, 50, 255))
                w_maxcb = datatext(1600, 950, 45, '/', Torus_Regular, anchor='mm')
                im = draw_text(im, w_maxcb)
                w_mapcb = datatext(1610, 950, 45, f'{map_maxcb}x', Torus_Regular, anchor='lm')
                im = draw_text(im, w_mapcb, color=(0, 255, 50, 255))

            #保存输出
            recent_img = f'recent_{uid}.png'
            outputImage_path = os.path.join(outputPath, recent_img)
            im.save(outputImage_path)

            msg = MessageSegment.image(f'file:///{os.path.abspath(outputPath + recent_img)}')
        except Exception as e:
            msg = f'制图错误:{e}'
    else:
        msg = False
    return msg

async def best_pfm(url, osuid, osumod, min, max, setmod=0):
    play_json = await osuapi(url)
    bp = []
    msg = ''
    if 'API' in play_json:
        msg = play_json
    elif play_json:
        if setmod != 0:
            modlist = set_mod_list(play_json, setmod)
            if not modlist:
                return '没有在bp上查询到开启该mod的成绩'
            max = len(modlist)
            modname = ','.join(resolve(setmod))
            bp.append(f"{osuid}'s Best Performance:\n{osumod} {modname} BP {min} - {max}")
            msg = "".join(bp)
            for num in modlist:
                s = play_json[num]
                pp = s['pp']
                mapid = s['beatmap_id']
                bp_msg = f'\nBP {num+1}  {pp}pp  id:{mapid}'
                bp.append(bp_msg)
                msg = "".join(bp)
        else:
            bp.append(f"{osuid}'s Best Performance:\n{osumod} BP {min} - {max}")
            msg = "".join(bp)
            for num in range(min-1, max):
                s = play_json[num]
                pp = s['pp']
                mapid = s['beatmap_id']
                bp_msg = f'\nBP {num+1}  {pp}pp  id:{mapid}'
                bp.append(bp_msg)
                msg = "".join(bp)
        return msg
    else:
        msg = False
    return msg

async def map_info(url, mapid, setmod):
    map_json = await osuapi(url)
    info = []
    msg = ''
    if 'API' in map_json:
        msg = map_json
    elif map_json:
        for i in map_json:
            bmapid = i['beatmapset_id']
            approved = i['approved']
            total_len = i['total_length']
            artist = i['artist_unicode']
            title = i['title_unicode']
            cs = i['diff_size']
            ar = i['diff_approach']
            od = i['diff_overall']
            hp = i['diff_drain']
            mode = i['mode']
            app_date = i['approved_date']
            creator = i['creator']
            bpm = i['bpm']
            source = i['source']
            if source == '':
                source = 'Nothing'
            version = i['version']
            stars = float(i['difficultyrating'])
            map_cb = i['max_combo']
        
        dirpath = await Download(bmapid)
        ver_file = get_file(dirpath, mapid, version)
        if mode == '0':
            map_pp = round(calc_acc_pp(ver_file, setmod)[5], 2)
        else:
            map_pp = 'Std Only'

        map_len = list(divmod(int(total_len), 60))
        map_len[1] = map_len[1] if map_len[1] >= 10 else f'0{map_len[1]}'
        music_len = f'{map_len[0]}:{map_len[1]}'

        app_num = approved_num[f'{approved}']
        stars = round(stars, 2)

        info.append(f'Query Map: {mapid} | Mode: {mod[mode].capitalize()}\n')
        info.append(f'Title: {title}\n')
        info.append(f'Artist: {artist}\n')
        info.append(f'Source: {source}\n')
        info.append(f'State: {app_num} | Song length: {music_len}\n')
        info.append(f'Version: {version} | Maper: {creator}\n')
        info.append(f'Approved Time: {app_date}\n')
        info.append(f'Stars: {stars} | CS: {cs} | AR: {ar} | OD: {od} | HP: {hp} | BPM: {bpm}\n')
        info.append(f'Max Combo: {map_cb} | SS PP: {map_pp}')

        msg = ''.join(info)
    else:
        msg = False
    return msg
