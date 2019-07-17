import json
import random
import socket
import time

from kazoo.client import KazooClient

from RPC.demo001 import InvalidOperation
from RPC.demo005 import ClientStub


class DistributedChannel(object):
    """
    支持zookeeper的连接 channel
    """
    def __init__(self):
        self._zk = KazooClient(hosts='127.0.0.1:2181')
        self._zk.start()
        self._get_servers()

    def _get_servers(self, event=None):
        """
        从zookeeper获取服务器地址信息列表
        """
        # 回调函数为 _get_servers
        # 在节点值有变化的时候 进行回调更新
        servers = self._zk.get_children('/rpc', watch=self._get_servers)
        print(servers)
        self._servers = []
        for server in servers:
            data = self._zk.get('/rpc/' + server)[0]
            addr = json.loads(data)
            self._servers.append(addr)

    def _get_server(self):
        """
        随机选出一个可用的服务器
        """
        return random.choice(self._servers)

    def get_connection(self):
        """
        提供一个可用的tcp连接
        """
        while True:
            # 随机选取一个可用的服务器
            server = self._get_server()
            print(server)
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((server['host'], server['port']))
            except ConnectionRefusedError:
                time.sleep(1)
                continue
            else:
                break
        return sock


if __name__ == "__main__":
    channel = DistributedChannel()

    for i in range(50):
        try:
            stub = ClientStub(channel)
            val = stub.divide(i)
        except InvalidOperation as e:
            print(e.message)
        else:
            print(val)
        time.sleep(1)

