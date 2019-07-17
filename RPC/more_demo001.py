import socket
import threading

from RPC.demo005 import ServerStub


class ThreadServer(object):
    def __init__(self, host, port, handlers):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = host
        self.port = port
        self.sock.bind((host, port))
        self.handlers = handlers

    def serve(self):
        """
        开始服务
        """
        self.sock.listen(128)
        print("开始监听")
        while True:
            conn, addr = self.sock.accept()
            print("建立链接%s" % str(addr))
            # 使用多线程的方式建立连接
            t = threading.Thread(target=self.handle, args=(conn,))
            t.start()

    def handle(self, client):
        stub = ServerStub(client, self.handlers)
        try:
            while True:
                stub.process()
        except EOFError:
            print("客户端关闭连接")

        client.close()
