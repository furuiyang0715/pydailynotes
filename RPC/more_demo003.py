import json
import socket
import sys
import threading
from kazoo.client import KazooClient

from RPC.demo001 import InvalidOperation
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
        self.register_zk()
        print("开始监听")
        while True:
            conn, addr = self.sock.accept()
            print("建立链接%s" % str(addr))
            # 多线程开启服务
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

    def register_zk(self):
        """
        注册到zookeeper
        """
        # 创建连接
        self.zk = KazooClient(hosts='127.0.0.1:2181')
        # 开启服务
        self.zk.start()
        # 创建根节点
        self.zk.ensure_path('/rpc')
        value = json.dumps({'host': self.host, 'port': self.port})
        # 创建服务子节点
        self.zk.create('/rpc/server', value.encode(), ephemeral=True, sequence=True)


class Handlers:
    @staticmethod
    def divide(num1, num2=1):
        """
        除法
        :param num1:
        :param num2:
        :return:
        """
        if num2 == 0:
            raise InvalidOperation()
        val = num1 / num2
        return val


if __name__ == '__main__':
    # 开启服务端进程
    # if len(sys.argv) < 3:
    #     print("usage:python server.py [host] [port]")
    #     exit(1)
    # host = sys.argv[1]
    # port = sys.argv[2]

    host = "localhost"
    port = 8899

    server = ThreadServer(host, int(port), Handlers)
    server.serve()
