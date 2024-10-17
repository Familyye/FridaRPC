项目名称: Frida RPC Android Hook Framework
项目简介:
本项目旨在使用 Frida RPC 框架 实现对 Android 应用的请求和响应报文的 Hook 和解密，主要针对全加密的 Android 应用进行渗透测试。通过该框架，用户能够监控和修改数据流，尤其是在应用层对数据进行了加密处理时，依然可以获取和解密报文数据。项目涵盖了请求和响应的拦截、解密、修改以及转发，适用于对应用数据安全的分析与测试。

功能特点:
Frida Hook: 通过 Frida 框架 Hook Android 应用的加密与解密函数，实现对 HTTP 请求体和响应体的监控与篡改。通过自定义的脚本，能够捕获并修改加密报文的数据，输出明文信息。

Hex 和 UTF-8 编码转换工具: 项目提供了 hex_string_to_utf8 和 utf8_to_hex_string 工具函数，用于在 16 进制字符串和 UTF-8 编码的字符串之间进行相互转换。此工具可以帮助处理应用中的编码问题，确保在发送和接收加密数据时，数据格式正确无误。

去除空格功能: no_space_string 函数专门用于处理特定键值对，如 mlds_model，去除键值中的空格字符，确保在渗透测试工具（如 Burp Suite）中传输时不会因为空格影响报文解析。

自定义 HTTP 服务器: 项目中包含了一个轻量级的 HTTP 服务器（基于 Python http.server 模块），用于接收并转发请求与响应包。服务器使用 BaseHTTPRequestHandler 来处理请求和响应，具备添加自定义头信息、读取请求体、以及原样返回报文的功能，便于测试过程中的数据调试。

Burp Suite 代理支持: 该项目通过设置 HTTP 代理，使得请求可以被转发到 Burp Suite 进行分析和篡改。同时，项目脚本会将修改后的请求发送回 Frida 进行进一步处理，实现对应用请求的持续监控和分析。

多线程支持: 项目使用多线程技术，在后台启动了一个镜像服务器来处理请求。这样可以同时进行请求拦截和篡改，而不会影响主线程的执行。

Frida 与 Python 集成: 脚本通过 Python 与 Frida 进行集成，允许开发者在远程设备上附加进程，并通过 Frida 脚本对应用进行 Hook 操作。通过 on_message 事件监听器，能够动态处理从 Frida 传递到 Python 的报文数据，实现动态篡改。

项目架构：
Frida Hook: 通过 Frida 对 Android 应用的加密函数进行 Hook，实现数据的捕获和解密。

HTTP 服务器: 本地启动一个自定义的 HTTP 服务器，负责接收从 Frida 捕获的请求和响应报文，并进行进一步处理或转发。

消息处理器: 使用 on_message 函数处理 Frida 发送的数据，并通过代理将其转发到 Burp Suite 或其他分析工具。

使用说明：
设置设备连接: 使用 frida.get_device_manager().add_remote_device('127.0.0.1:26666') 将设备连接到本地 Frida 服务器。

加载 Frida 脚本: 打开 Frida 脚本文件 dodonew.js，并将其通过 process.create_script() 加载到目标应用的进程中。

启动服务器: 运行 echo_server_thread() 来启动本地的 HTTP 服务器，监听端口 28080，用于接收并转发请求。

使用代理工具进行分析: 项目提供了 Burp Suite 代理支持，通过 proxies = {'http': 'http://127.0.0.1:8080'} 设置代理，使得所有请求和响应都可以通过 Burp Suite 进行调试与篡改。

修改与转发请求: 捕获的请求与响应数据会被转发至服务器，同时你可以通过 Frida 提供的 script.post() 来动态修改请求和响应，完成对应用报文的分析和渗透测试。

依赖项：
Frida: 需要安装 Frida，用于 Hook Android 应用的进程。
Requests: 用于向本地服务器发送 HTTP 请求。
Python 3.x: 脚本使用 Python 编写，并依赖 Python 的多线程和 HTTP 服务器模块。

适用场景:
渗透测试: 本项目适用于对安卓应用的安全测试，特别是对加密流量的解密与分析。
应用分析: 开发者或安全研究人员可以通过该框架深入分析应用的数据加密机制，验证其安全性。
