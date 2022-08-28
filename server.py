import socket
import json
import sys
import rich.console
import traceback
import os
from urllib.request import urlopen
import threading
import os.path
import time
import keyboard
import urllib.parse

console = rich.console.Console()
__ver__ = "1.5"
argv = sys.argv
config = {}

wd = __file__.split(os.sep)
workingDir = ""
for w in wd[0:-1]:
    workingDir += w
    workingDir += os.sep

# 解析报文
def parseLocalPath(msg) -> str:
    global config
    p = urllib.parse.unquote(msg)
    if msg[0] == "/":
        p = p[1:]
    p = os.path.join(config["server"]["root"], p)
    if os.path.isdir(p):
        fileList = os.listdir(p)
        for f in config["default"]:
            if f in fileList:
                p = os.path.join(p, f)
                break
    return p    

def analysisRequestData(msg, a) -> dict:
    req_d = msg.split(" ")
    # 寻找参数
    if req_d[0] == "POST":
        _arg = a[1]
    else:
        _start = req_d[1].find("?")
        if _start != -1:
            _arg = req_d[1][_start + 1:]
            req_d[1] = req_d[1][:_start]
        else:
            _arg = ""
    # 解析
    request_data = {
        "mode":req_d[0],
        "path":parseLocalPath(req_d[1]),
        "protocol":req_d[2],
        "args":urllib.parse.parse_qs(_arg)
    }
    return request_data

def analysisHeader(msg) -> dict:
    headers = msg       # msg.split("\r\n")
    header = {}
    for h in headers:
        t = h.split(": ")
        header[t[0]] = t[1]
    return header

def analysisMsg(message) -> dict: 
    """analysisMsg(String: message) -> dict"""
    global console, inUse
    msg = message.split("\r\n\r\n")
    _msg = msg[0].split("\r\n")
    # 组成
    recv_data = analysisRequestData(_msg[0],msg)
    # console.log(_msg)
    recv_data["header"] = analysisHeader(_msg[1:])
    
    return recv_data  

# 读取页面
def readFile(path) -> tuple:
    global config
    file = b""
    status = 200
    try:
        with open(path, "rb") as f:
            file = f.read()
        status = 200
    except FileNotFoundError:
        status = 404
        with open(config["error"][404], "rb") as f:
            file = f.read()
            file += ("<center>" + path + "</center>").encode()
    return file, status

def getFileType(path, status) -> str:
    if status == 200:
        return path.split(".")[-1]
    else:
        return "html"

# 执行py
print_text = "" 
inUse = False
class newstdout:
    def write(text):# (self,text):
        global print_text    # 这里是执行stdout后的代码 
        print_text += text
        
    def fileno():# (self,text):
        pass
    def flush():
        pass
        # global print_text
        # print_text = ""
oldstdout = sys.stdout
pageData = {}

def initPyPage(code):
    # code1 = "if True:\n" + code
    code1 = code
            
    return code1.replace("sdk.", "")

def initH2P(code):
    return code.strip().replace("sdk.", "")


def runPyPage(code, recv_data) -> tuple:
    global print_text, oldstdout, inUse, pageData
    file = b""
    status = 200
    while inUse:     # 排队
        time.sleep(0.1)
    inUse = True
    try:
        print_text = ""
        sys.stdout = newstdout
        exec(initPyPage(code))
        file = print_text.encode()
    except:
        file = str(traceback.format_exc()).encode()
        status = 500
    sys.stdout = oldstdout
    inUse = False
    return file, status
a = ""
def runPyIn(code, recv_data) -> str:
    global print_text, pageData, oldstdout, a, console
    start = code.find("<?py")
    html = ""
    if start != -1:
        end = code.find("?>", start)
        pycode = code[start + 4:end]
        a = pycode
        print_text = ""
        exec(initPyPage(pycode))
        html = code[:start]
        html += print_text
        html += code[end + 2:]
        return runPyIn(html, recv_data)
    else:
        return code

def runPyIn_eval(code, recv_data) -> str:
    global print_text, pageData, oldstdout, a, console
    start = code.find("<?pyeval")
    html = ""
    if start != -1:
        end = code.find(">", start)
        pycode = code[start + 8:end]
        html = code[:start]
        html += str(eval(initH2P(pycode)))
        html += code[end + 1:]
        return runPyIn_eval(html, recv_data)
    else:
        return code

def runPyInPage(code, recv_data) -> tuple:
    global print_text, oldstdout, inUse, a
    file = b''
    status = 200
    while inUse:     # 排队
        time.sleep(0.1)
    inUse = True
    try:
        sys.stdout = newstdout
        file = runPyIn(runPyIn_eval(code, recv_data), recv_data).encode()
    except:
        file = str(traceback.format_exc()).encode()
        status = 500
    sys.stdout = oldstdout
    console.log(a)
    inUse = False
    return file, status

# 处理请求
def handle(sock, addr):
    global console, config, inUse
    try:
        recv_data = analysisMsg(sock.recv(1024).decode())            # 解析请求报文
        file, status = readFile(recv_data["path"])          # 读取文件
        fileType = getFileType(recv_data["path"], status)   # 截取文件后缀
        
        if status == 200:
            if fileType == "py":
                file, status = runPyPage(file.decode(), recv_data)
            elif fileType == "h2p" or fileType == "h5p":
                file, status = runPyInPage(file.decode(), recv_data)
            
        resp_data = f"{recv_data['protocol']} {status} {config['HttpCodeMsg'][str(status)]}\r\n\r\n".encode()
        resp_data += file

        sock.send(resp_data)
        sock.close()
        
    except:
        while inUse:       # 排队
            time.sleep(0.1)
        inUse = True
        console.print_exception(show_locals=True)
        inUse = False
    
    while inUse:
        time.sleep(0.1)
    inUse = True
    try:
        console.log(recv_data)
    except:
        pass
    inUse = False

def exit_server(addr):
    global console, inUse
    urlopen(f"http://{addr}")
    while inUse:
        time.sleep(0.1)
    inUse = True
    console.log("已尝试退出")
    inUse = False

def server():
    global config, console
    keyboard.add_hotkey("ctrl+c", lambda: exit_server(f'{config["server"]["ip"]}:{config["server"]["port"]}'))
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # tcp_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_client.bind((config["server"]["ip"], config["server"]["port"]))
    tcp_client.listen(config["server"]["max"])
    console.log(f'[green]服务器已在 {config["server"]["ip"]}:{config["server"]["port"]} 开启')

    while True:
        sock, addr = tcp_client.accept()
        t = threading.Thread(None, lambda: handle(sock, addr))
        # t.setDaemon(True)
        t.start()

def initServer():
    global config, workingDir
    config = json.load(open("server.json"))
    config["HttpCodeMsg"] = {
        "200":"OK",
        "404":"Not Found\r\nContent-Type: text/html",
        "500":"Internal Server Error"
    }
    config["error"] = {
        404: os.path.join(workingDir, "error/404.html")
    }
    for c in config["server"]["error"]:
        config["error"][c["code"]] = c["file"]

def parseArgs(argv) -> dict:
    global console
    args = {"c":"."}
    args["Program"] = argv[0]
    args["mode"] = argv[1]
    args["opt"] = []
    # console.print(argv,argv.__len__())
    """if argv.__len__() >= 3:
        arg = argv[2:]
        while arg.__len__() == 0:
            a = arg[0]
            arg.pop(0)
            print(a)
            if arg.__len__() < 0:
                if arg[0][:1] != "-":
                    args[a] = arg[0]
                    arg.pop(0)
                else:
                    args["opt"] += [a]"""
    if argv.__len__() >= 3:
        if argv[2] == "-c":
            args["c"] = argv[3]
    return args

def createGuide() -> None:
    global console, __ver__
    config = {}
    config["name"] = console.input("服务器名：")
    config["server"] = {}
    config["server"]["ip"] = console.input("主机名（IP）：")
    config["server"]["port"] = int(console.input("端口："))
    config["server"]["root"] = console.input("根目录：")
    config["server"]["max"] = int(console.input("最大连接数（推荐：1024）："))
    console.print("正在创建服务器配置 . . .")
    config["default"] = [
        "index.html",
        "index.py",
        "index.h2p"
    ]
    config["server"]["error"] = []
    json.dump(config, open("server.json", "w", encoding = "utf-8"))
    console.print("--- server.json ---")
    console.print(config)
    console.print("--- 结尾：server.json ---")
    console.print("创建完成，稍后您可以在",os.path.abspath(os.path.join(os.curdir, "server.json")),"修改服务器配置")
    console.print("正在初始化目录 . . .")
    os.mkdir(config["server"]["root"])
    with open(os.path.join(config["server"]["root"], "index.html"), "w", encoding = "utf-8") as f:
        f.write(f"""
<center>
    <h1>欢迎使用 XWebServer+！</h1>
    <p>如果您看到这个页面，代表服务器已创建成功</p>
    <hr>
    <p>XWebServer+/{__ver__}</p>
</center>""")
    console.print(f"服务器创建完成！您可以使用 [yellow]python server.py -c {os.path.abspath(os.curdir)} [/]启动")



if __name__ == "__main__":
    args = parseArgs(argv)
    # console.print("[yellow]建议使用 任务管理器/htop 直接杀死 python 进程来停止 XWebServer+")
    if args["mode"] == "about":
        console.print(f"""XWebServer+ V{__ver__}
作者：这里是小邓
官网：https://xiaodeng.tk
贡献名单：
    StarWorld
        设计思路""")
    elif args["mode"] == "help":
        console.print(f"""帮助 —— XWebServer+
python server.py <操作> [<选项>...]

    help：帮助
    about：关于
    create：服务器创建向导
    start：开启服务器
        -c <path>   指定服务器配置所在路径""")
    elif args["mode"] == "start":
        os.chdir(args["c"])
        initServer()
        server()
    elif args["mode"] == "create":
        console.print("XWebServer+ 服务器创建向导")
        dir = console.input("您打算在哪里创建服务器？")
        if os.path.isdir(dir) == False:
            os.mkdir(dir)
        os.chdir(dir)
        createGuide()
    else:
        console.print("未知操作")
