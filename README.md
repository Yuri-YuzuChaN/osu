# osu

基于HoshinoBot v2的osu查询模块

项目地址：https://github.com/Yuri-YuzuChaN/osu

## 使用方法

1. 将该项目放在HoshinoBot插件目录 `modules` 下，或者clone本项目 `git clone https://github.com/Yuri-YuzuChaN/osu`
2. ~~在`config.json`文件中添加`apikey`，mysql数据库地址`sql_host`，数据库名`sql_name`、表名`sql_table`、用户名`sql_user`和密码`sql_pwd`，根据自己的机器配置填入~~
2. 在`api.py`填入申请的`apikey`
3. pip以下依赖：`pillow` ~~`oppai`~~
4. 在`config/__bot__.py`模块列表中添加`osu`
5. 重启HoshinoBot

**注：`pillow`需要高于等于8.0.0版本，`oppai`模块已自带~~`oppai`在windows系统下需要`C++ 14.0`才可安装~~**

## 指令说明

- `[osuhelp]`发送指令大全图片
- `[info]`查询自己
- `[info :num]`查询自己在某模式的信息
- `[info user]`查询某位玩家
- `[info user :num]`查询某位玩家在某模式的信息
- `[bind user]`绑定
- `[unbind]`解绑
- `[mode num]`更改查询的默认模式
- `[update osuid user]`更改绑定的用户名
- `[update icon]`更新头像
- `[recent]`查询自己在最近游玩的成绩
- `[recent :num]`查询自己在最近游玩某模式的成绩
- `[recent user]`查询某位玩家在最近游玩的成绩
- `[recent user :num]`查询某位玩家在最近游玩某模式的成绩
- `[score mapid]`查询自己在该地图的成绩
- `[score mapid :num]`查询自己在该地图某模式的成绩
- `[score user mapid]`查询某位玩家在该地图的成绩
- `[score user mapid :num]`查询某位玩家在该地图某模式的成绩
- `num` ： `0` std, `1` taiko, `2` ctb, `3` mania

**注：目前bug较多，尽量不要查询除std以外模式。发送的图片中的if fc pp可能有错误**

## 存在问题

1. `pp计算`可能有错误

## 饼

1. 查询 `bp`

## 更新说明

**2021-01-11**
1. 插件已自带pp计算模块`oppai`
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
