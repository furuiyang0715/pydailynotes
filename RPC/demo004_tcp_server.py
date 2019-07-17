import socket

# # 编写一个 TCP 服务端
# sock = socket.socket()  # 创建一个套接字
# sock.bind()  # 绑定端口
# sock.listen()  # 监听连接
# sock.accept()  # 接受新连接
# sock.close()  # 关闭服务器套接字
#
#
# # 编写一个 TCP 客户端
# sock = socket.socket()  # 创建一个套接字
# sock.connect()  # 连接远程服务器
# sock.recv() # 读
# sock.send()  # 尽可能地写
# sock.sendall()  # 完全写
# sock.close()  # 关闭

# 使用 TCP 来实现传输控制

import socket


class Channel(object):
    """
    连接通道
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def get_connection(self):
        """
        获取一个 tcp 连接
        :return:
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        return sock


class Server(object):
    """
    服务器
    """
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = host
        self.port = port
        self.sock.bind((host, port))
