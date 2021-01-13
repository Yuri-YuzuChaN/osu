# osu

基于HoshinoBot v2的osu查询模块

项目地址：https://github.com/Yuri-YuzuChaN/osu

## 使用方法

1. 将该项目放在HoshinoBot插件目录 `modules` 下，或者clone本项目 `git clone https://github.com/Yuri-YuzuChaN/osu`
2. ~~在`config.json`文件中添加`apikey`，mysql数据库地址`sql_host`，数据库名`sql_name`、表名`sql_table`、用户名`sql_user`和密码`sql_pwd`，根据自己的机器配置填入~~
3. 在`api.py`填入申请的`apikey`
4. pip以下依赖：`pillow` ~~`oppai`~~
5. 在`config/__bot__.py`模块列表中添加`osu`
6. 重启HoshinoBot

**注：`pillow`需要高于等于8.0.0版本，`oppai`模块已自带，`oppai`目前必须在`py38 64bit`环境下才可运行**
~~`oppai`在windows系统下需要`C++ 14.0`才可安装~~

## 指令说明

- `[info]`查询自己的信息
- `[info :mode]`查询自己在 mode 模式的信息
- `[info user]`查询 user 的信息
- `[info user :mode]`查询 user 在 mode 模式的信息
- `[bind user]`绑定用户名 user
- `[unbind]`解绑
- `[mode mode]`更改默认查询的模式
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
- `[bp num]`查询自己bp榜第 num 的成绩
- `[bp user num]`查询 user bp榜第 num 的成绩
- `[bp list min-max]`查询自己bp榜第 min 到 max 的成绩
- `[bp list user min-max]`查询 user bp榜第 min 到 max 的成绩
- `mode` : `0 `std, `1` taiko, `2` ctb, `3` mania

**注：目前bug较多，尽量不要查询除std以外模式。发送的图片中的if fc pp可能有错误**

## 存在问题

1. `pp计算`可能有错误
2. 开启DT HR时OD计算可能有错误

## 即将实现

1. fail成绩下的地图时长

## 更新说明

**2021-01-13**
1. 新增成绩信息的地图时长 **目前仅能显示pass成绩的时长，fail成绩还未实现**
2. *`bp`指令可查询其它模式 **例:`bp3 list 1-6` 为 查询 `mania` 的bp 1-6，`bp3`中的`3`为模式，可参考指令大全中的`mode`参数，如果单独输入bp3功能与bp 3相同**
3. 修复个别用户没有自定义头图的情况下无法下载头图的问题
4. 修复NC和DT共存的问题

***1.目前仅能显示pass成绩的时长，fail成绩还未实现***
***2.bp示例:`bp3 list 1-6` 为 查询 `mania` 的bp 1-6，`bp3`中的`3`为模式，可参考指令大全中的`mode`参数，如果单独输入bp3功能与bp 3相同***

**2021-01-12**

1. 新增`bp`指令，使用方法见指令说明
2. 修复找不到地图BG的问题
3. 修复无法下载个人头图的问题

**2021-01-11**

1. 插件已自带pp计算模块`oppai`，需在`py38 64bit`环境下才可运行
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
