import argparse
import urllib
from urllib.parse import quote, unquote
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import requests
import frida
import re

# 定义一个继承自BaseHTTPRequestHandler的请求处理类
class RequestHandler(BaseHTTPRequestHandler):

    # 处理请求方法
    def do_REQUEST(self):
        content_length = int(self.headers.get('content-length', 0))  # 获取请求体长度
        self.send_response(200)  # 设置响应状态码为200
        self.send_header('Content_Length', str(content_length))  # 添加响应头
        self.send_header('X-Mirror-Server', 'True')
        self.send_header('TMF_apiName', self.headers.get('TMF_apiName'))  # 获取并设置请求中的TMF_apiName头
        self.end_headers()  # 结束头部设置
        self.wfile.write(self.rfile.read(content_length))  # 将请求体数据作为响应体返回

    # 处理响应方法
    def do_RESPONSE(self):
        content_length = int(self.headers.get('content-length', 0))  # 获取响应体长度
        self.send_response(200)  # 设置响应状态码为200
        self.send_header('Content_Length', str(content_length))  # 添加响应头
        self.send_header('X-Mirror-Server', 'True')
        self.end_headers()  # 结束头部设置
        self.wfile.write(self.rfile.read(content_length))  # 将响应体数据返回给客户端

# 启动回显服务器
def echo_server_thread():
    print('start echo server at port {}'.format(28080))
    server = HTTPServer(('', 28080), RequestHandler)
    server.serve_forever()  # 永久运行服务器

# 使用线程启动镜像服务器
t = Thread(target=echo_server_thread)
t.daemon = True  # 设置为守护线程
t.start()

proxies = {'http': 'http://127.0.0.1:8080'}  # 设置代理

# 处理 Frida 中发送的数据
def on_message(message, data):
    if message['type'] == 'send':  # 处理从 JS 发送来的数据
        payload = message['payload']
        TAG = payload['TAG']

        # 处理请求数据
        if TAG == 'Request':
            RequestBody = unquote(payload["RequestBody"])  # 解码请求体
            requestHeaders = {'X-Turbo_Intruder': 's'}  # 设置请求头
            requestURL = "http://127.0.0.1:28080/Request/"  # 发送到镜像服务器的URL
            request = requests.request("REQUEST", requestURL, proxies=proxies, headers=requestHeaders, data=RequestBody.encode("utf-8"))  # 发送请求
            request.encoding = 'utf-8'  # 设置编码
            script.post({"modify_requestBody": request.text})  # 将修改后的请求体发送给JS

        # 处理响应数据
        elif TAG == 'Response':
            ResponseBody = payload["ResponseBody"]  # 获取响应体
            responseURL = "http://127.0.0.1:28080/Response"  # 发送到镜像服务器的URL
            response = requests.request("RESPONSE", responseURL, proxies=proxies, data=ResponseBody.encode('utf-8'))  # 发送响应
            script.post({"modify_responseBody": response.text})  # 将修改后的响应体发送给JS
    else:
        print("error", message)  # 错误处理

# 连接到远程设备并附加到进程
process = frida.get_device_manager().add_remote_device('127.0.0.1:26666').attach('嘟嘟牛在线')

# 读取并加载JS脚本
with open("dodonew.js", "r", encoding='utf-8') as f:
    js_code = f.read()
script = process.create_script(js_code)

# 监听来自JS的消息
script.on('message', on_message)
script.load()  # 加载脚本
sys.stdin.read()  # 保持主线程运行
