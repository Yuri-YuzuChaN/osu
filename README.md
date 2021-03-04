# osu

基于HoshinoBot v2的osu查询模块

项目地址：https://github.com/Yuri-YuzuChaN/osu

## 使用方法

1. 将该项目放在HoshinoBot插件目录 `modules` 下，或者clone本项目 `git clone https://github.com/Yuri-YuzuChaN/osu`
2. 在`api.py`填入申请的`apikey`，`apikey`申请地址：https://osu.ppy.sh/p/api/
3. pip以下依赖：`pillow`，`oppai`，`pyttanko`
4. 在`config/__bot__.py`模块列表中添加`osu`
5. 重启HoshinoBot

**注：`pillow`需要高于等于8.0.0版本，Windows环境下`oppai`模块已自带，`oppai`目前必须在`py38 64bit`环境下才可运行**

**如果环境为Linux，请`pip install oppai`，并将`osu_pp.py`中`.oppai.oppai`改为`oppai`**

## 指令说明

- `[info]`查询自己的信息
- `[info :mode]`查询自己在 mode 模式的信息
- `[info user]`查询 user 的信息
- `[info user :mode]`查询 user 在 mode 模式的信息
- `[bind user]`绑定用户名 user
- `[unbind]`解绑
- `[update mode mode]`更改默认查询的模式
- `[update osuid user]`更改绑定的用户名 user
- `[update icon]`更新自己头像和头图
- `[recent]`查询自己最近游玩的成绩
- `[recent :mode]`查询自己最近游玩 mode 模式的成绩
- `[recent user]`查询 user 最近游玩的成绩
- `[recent user :mode]`查询 user 最近游玩 mode 模式的成绩
- `[score mapid]`查询自己在 mapid 的成绩
- `[score mapid :mode]`查询自己在 mapid  mod 模式的成绩
- `[score user mapid]`查询 user 在 mapid 的成绩
- `[score user mapid :mode]`查询 user 在 mapid  mode 模式的成绩
- `[map mapid]`查询 mapid 地图的信息
- `[bp num]`查询自己bp榜第 num 的成绩
- `[bp user num]`查询 user bp榜第 num 的成绩
- `[bp list min-max]`查询自己bp榜第 min 到 max 的成绩
- `[bp list user min-max]`查询 user bp榜第 min 到 max 的成绩
- `mode` : `0 `std, `1` taiko, `2` ctb, `3` mania
- bp扩展 `bp`: std, `bp1`: taiko, `bp2`: ctb, `bp3`: mania

**除`std`模式外，查询其它模式需带上`mode`**

## 存在问题

1. 开启DT HR时OD计算可能有错误

## 即将实现

1. ~~pp+数据~~

## 更新说明

**2021-03-04**
1. bp指令可以查询带mod的排行榜
2. map指令可以计算带mod的数据及pp
**示例：`bp 1 +DT,HD`，查询BP中加DT和HD第一位的成绩，map指令相同**

**2021-03-03**
1. 修复无法更新头像和头图的问题

**2021-02-20**
1. 更新显示std外的acc以及颜色

**2021-02-12**
1. 更新pp计算模块

**2021-01-26**
1. 由于`zipfile`模块在解压文件名过长的文件时无法完全解压，已将文件名修改地图ID

**2021-01-25**
1. 可以查询其它模式
2. 修改更改默认查询的模式的指令，现指令为`update mode mode`

**2021-01-24**
1. 修复大部分旧地图获取不到文件的问题

**2021-01-21**
1. 更新致命bug，获取osz文件失败，在计算PP的时候，导致bot程序退出的问题，必须更新

**2021-01-19**
1. 新增查询地图信息指令`map`

**2021-01-15**

1. 新增成绩信息包括Fail成绩的地图时长
2. 修复ifpp计算错误的问题
3. 下载地图改为不含视频版

**2021-01-13**

1. 新增成绩信息的地图时长
2. `bp`指令可查询其它模式 
3. 修复个别用户没有自定义头图的情况下无法下载头图的问题
4. 修复NC和DT共存的问题

**2021-01-12**

1. 新增`bp`指令，使用方法见指令说明
2. 修复找不到地图BG的问题
3. 修复无法下载个人头图的问题

**2021-01-11**

1. 插件已自带pp计算模块`oppai`，需在`py38 64bit`环境下才可运行，Linux环境请查看使用方法
2. 修复`mode`指令错误的问题

**2021-01-09**

1. 修复计算acc 95-100 pp错误的问题
2. 修复绑定失败的问题
3. 修复`info`图经验条长度错误的问题
4. 修复地图存在但又重新下载的问题
5. 添加`info`图的`个人头图`、`总命中次数`和`总游玩时长`
6. 不再保存裁切图片
7. 不再重复下载头像

**2021-01-06**

1. 全异步执行，防止拥堵

**2021-01-03**

1. 移除`draw_recent`函数

**2021-01-02**

1. 数据库改用`sqlite3`，弃用`MYSQL`
2. 删除`config.json`
