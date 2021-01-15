import time
from .oppai.oppai import *


# 计算95-100acc的pp
def calculation_acc_pp(osufile, mods_num):
    pp = []

    ez = ezpp_new()
    ezpp_set_autocalc(ez, 1)

    osz = open(osufile, 'r', encoding='utf-8')
    data = osz.read()
    osz.close()

    ezpp_data_dup(ez, data, len(data.encode('utf-8')))
    ezpp_set_mods(ez, mods_num)
    for acc in range(95, 101):
        ezpp_set_accuracy_percent(ez, acc)
        pp.append(ezpp_pp(ez))
    ezpp_free(ez)

    return pp

# 计算游玩pp
def calculation_pp(osufile, mods_num, maxcb, c50, c100, c300, miss):
    # cb总和
    setcb = c50 + c100 + c300 + miss

    map = ezpp_new()
    ezpp_set_autocalc(map, 1)
    ezpp_dup(map, osufile)

    # 输入mods
    ezpp_set_mods(map, mods_num)
    # 计算开始计算pp前的难度
    map_stars = ezpp_stars(map)
    # 输入最大连击cb数
    ezpp_set_combo(map, maxcb)
    # 输入cb包括miss总和 
    ezpp_set_end(map, setcb)
    # 输入100和50数量 计算acc
    ezpp_set_accuracy(map, c100, c50)
    # 输入miss数量
    ezpp_set_nmiss(map, miss)
    
    cs = ezpp_cs(map)
    ar = ezpp_ar(map)
    od = ezpp_od(map)
    hp = ezpp_hp(map)
    play_pp = round(ezpp_pp(map), 2)
    aim_pp = round(ezpp_aim_pp(map), 2)
    speed_pp = round(ezpp_speed_pp(map), 2)
    acc_pp = round(ezpp_acc_pp(map), 2)
    acc = round(ezpp_accuracy_percent(map), 2)

    ezpp_free(map)
    return map_stars, cs, ar, od, hp, play_pp, aim_pp, speed_pp, acc_pp, acc

def calc_if(osufile, mods_num, c50, c100, mapcb):
    map = ezpp_new()
    ezpp_set_autocalc(map, 1)
    ezpp_dup(map, osufile)
    ezpp_set_mods(map, mods_num)
    ezpp_set_combo(map, mapcb)
    ezpp_set_accuracy(map, c100, c50)
    if_pp = ezpp_pp(map)
    ezpp_free(map)
    return if_pp

def calc_time(osufile, c50, c100, c300, miss):
    setcb = c50 + c100 + c300 + miss
    map = ezpp_new()
    ezpp_dup(map, osufile)
    play_time = ezpp_time_at(map, setcb)
    return play_time
