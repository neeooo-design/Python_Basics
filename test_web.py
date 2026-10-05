# 4. 本地接口测试：练自动化测试
# 用 http.server 写一个仅供测试的小服务，提供 GET /health，返回 JSON {"status": "ok"}。
# 用 unittest 和 urllib.request 验证状态码、Content-Type 和响应体；再测试未知路径返回 404。
# 测试结束时要关闭服务，保证重复运行不会因端口占用而失败。

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading
import unittest
from urllib.error import HTTPError
import urllib.request


class HealthHandler(BaseHTTPRequestHandler):
    """请求处理器：处理客户端发来的 HTTP GET 请求"""

    def do_GET(self):
        # 1. 如果请求路径是 /health，返回 200 和 json 数据
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
        # 2. 如果是其他未定义路径，返回 404
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        """静音默认控制台日志，避免测试输出被 HTTP 访问日志打乱"""
        pass


class TestHealthServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """测试类开始前执行：启动后台 HTTP 服务"""
        # 绑定端口 0，由操作系统自动分配未被占用的空闲端口
        cls.server = HTTPServer(("127.0.0.1", 0), HealthHandler)
        cls.port = cls.server.server_port
        cls.base_url = f"http://127.0.0.1:{cls.port}"

        # 在独立的后台守护线程中启动服务，防止主线程卡死
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        """所有测试结束后执行：关闭服务并释放端口"""
        cls.server.shutdown()      # 停止接收请求循环
        cls.server.server_close()  # 关闭套接字，释放端口资源
        cls.thread.join()          # 等待后台线程完全退出

    def test_health_success(self):
        """测试 GET /health 接口的状态码、Content-Type 和响应内容"""
        url = f"{self.base_url}/health"

        with urllib.request.urlopen(url) as response:
            # 1. 验证状态码是否为 200
            self.assertEqual(response.status, 200)

            # 2. 验证响应头中的 Content-Type 是否为 application/json
            content_type = response.headers.get("Content-Type")
            self.assertEqual(content_type, "application/json")

            # 3. 验证响应体内容反序列化后是否为 {"status": "ok"}
            body_bytes = response.read()
            body_str = body_bytes.decode("utf-8")
            data = json.loads(body_str)
            self.assertEqual(data, {"status": "ok"})

    def test_unknown_path_returns_404(self):
        """测试访问未知路径返回 404"""
        url = f"{self.base_url}/unknown_path"

        # urllib.request 遇到 404 等错误状态码时会自动抛出 HTTPError 异常
        with self.assertRaises(HTTPError) as cm:
            urllib.request.urlopen(url)

        # 验证抛出的异常状态码是 404，并主动关闭异常持有的连接资源
        self.assertEqual(cm.exception.code, 404)
        cm.exception.close()
