from .oppai.oppai import *

# 计算95-100acc的pp
def calc_acc_pp(osufile, mods_num):
    pp = []
    
    ez = ezpp_new()
    ezpp_set_autocalc(ez, 1)
    ezpp_dup(ez, osufile)
    ezpp_set_mods(ez, mods_num)
    for acc in range(95, 101):
        ezpp_set_accuracy_percent(ez, acc)
        pp.append(int(ezpp_pp(ez)))
    ezpp_free(ez)

    return pp

# 计算游玩pp
def calc_pp(osufile, mods_num, maxcb, c50, c100, c300, miss):
    # cb总和
    setcb = c50 + c100 + c300 + miss

    ez = ezpp_new()
    ezpp_set_autocalc(ez, 1)
    ezpp_dup(ez, osufile)

    # 输入mods
    ezpp_set_mods(ez, mods_num)
    # 计算开始计算pp前的难度
    map_stars = ezpp_stars(ez)
    # 输入最大连击cb数
    ezpp_set_combo(ez, maxcb)
    # 输入cb包括miss总和 
    ezpp_set_end(ez, setcb)
    # 输入100和50数量 计算acc
    ezpp_set_accuracy(ez, c100, c50)
    # 输入miss数量
    ezpp_set_nmiss(ez, miss)
    
    cs = ezpp_cs(ez)
    ar = ezpp_ar(ez)
    od = ezpp_od(ez)
    hp = ezpp_hp(ez)
    play_pp = round(ezpp_pp(ez), 2)
    aim_pp = int(round(ezpp_aim_pp(ez), 2))
    speed_pp = int(round(ezpp_speed_pp(ez), 2))
    acc_pp = int(round(ezpp_acc_pp(ez), 2))
    acc = round(ezpp_accuracy_percent(ez), 2)

    return map_stars, cs, ar, od, hp, play_pp, aim_pp, speed_pp, acc_pp, acc

def calc_if(osufile, mods_num, c50, c100, mapcb):
    ez = ezpp_new()
    ezpp_set_autocalc(ez, 1)
    ezpp_dup(ez, osufile)
    ezpp_set_mods(ez, mods_num)
    ezpp_set_combo(ez, mapcb)
    ezpp_set_accuracy(ez, c100, c50)
    if_pp = ezpp_pp(ez)
    ezpp_free(ez)
    return if_pp

def calc_time(osufile, c50, c100, c300, miss):
    setcb = c50 + c100 + c300 + miss
    ez = ezpp_new()
    ezpp_dup(ez, osufile)
    play_time = ezpp_time_at(ez, setcb)
    ezpp_free(ez)
    return play_time
