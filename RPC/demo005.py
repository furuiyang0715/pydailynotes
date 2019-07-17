import socket

from RPC.demo003 import DivideProtocol, InvalidOperation, MethodProtocol


class ClientStub(object):
    """
    客户端存根
    """
    def __init__(self, channel):
        self.channel = channel
        self.conn = self.channel.get_connection()

    def divide(self, num1, num2=1):
        # 构造
        proto = DivideProtocol()
        args = proto.args_encode(num1, num2)
        self.conn.sendall(args)
        result = proto.result_decode(self.conn)
        if isinstance(result, InvalidOperation):
            raise result
        else:
            return result


class ServerStub(object):
    def __init__(self, connection, handlers):
        """
        服务器存根
        :param connection: 与客户端的socket连接
        :param handlers: 存放被调用的方法
        """
        self._process_map = {
            'divide': self._process_divide,
        }
        self.conn = connection
        self.method_proto = MethodProtocol(self.conn)
        self.handlers = handlers

    def process(self):
        """
        被服务器调用的入口，服务器收到请求后调用该方法
        """
        # 获取解析调用请求的方法名
        name = self.method_proto.get_method_name()

        # 调用对应的处理方法
        self._process_map[name]()

    def _process_divide(self):
        """
        执行divide本地调用，并将结果返回给客户端
        """
        # 接收调用参数
        proto = DivideProtocol()
        args = proto.args_decode(self.conn)

        # 进行本地divide调用
        try:
            result = self.handlers.divide(**args)
        except InvalidOperation as e:
            result = e

        # 构造返回值消息并返回
        result = proto.result_encode(result)
        self.conn.sendall(result)


class Server(object):
    """socket 服务器"""
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
            stub = ServerStub(conn, self.handlers)
            try:
                while True:
                    stub.process()
            except EOFError:
                print("客户端关闭连接")
            # 关闭服务端连接
            conn.close()


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
    server = Server('127.0.0.1', 8888, Handlers)
    server.serve()
