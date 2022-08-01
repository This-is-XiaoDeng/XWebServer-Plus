# 创建服务器

> 如果您看得懂人话并知道如何使用 XWebServer+ 创建并开始服务器，请自觉下一章

## 创建服务器

使用指令 `python server.py create` 进入服务器创建向导

### 两个目录

|名称            |描述                        |
|----------------|---------------------------|
|服务器根目录     |服务器源码根目录             |
|服务器配置目录   |服务器 `server.json` 所在目录|

## 完成创建

整体输出看起来像这样

```bash
XWebServer+ 服务器创建向导
您打算在哪里创建服务器？./demo_server
服务器名：DemoServer
主机名（IP）：127.0.0.1
端口：19132
根目录：./src
最大连接数（推荐：1024）：1024
正在创建服务器配置 . . .
--- server.json ---
{
    'name': 'DemoServer',
    'server': {'ip': '127.0.0.1', 'port': 19132, 'root': './src', 'max': 1024, 'error': []},
    'default': ['index.html', 'index.py', 'index.h2p']
}
--- 结尾：server.json ---
创建完成，稍后您可以在 C:\Users\这里是小邓\Desktop\Projects\XWebServer+\demo_server\server.json 修改服务器配置
正在初始化目录 . . .
服务器创建完成！您可以使用 python server.py -c <=××××××××××××××××××××××=>\demo_server 启动
```

### 注意事项

1. 向导中输入的根目录是相对于配置目录的
2. XWebServer+ 会覆盖已存在的 `server.json` （如果有的话）
3. 输出最后的启动指令是错的估计最近会修掉