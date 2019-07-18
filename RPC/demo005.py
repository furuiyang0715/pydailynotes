import socket

import struct

from io import BytesIO


class InvalidOperation(Exception):
    """
    自定义非法操作异常
    """
    def __init__(self, message=None):
        self.message = message or "Invalid operation."


class DivideProtocol(object):
    """
    float divide(1: int num1, 2: int num2=1)
    """
    conn = None

    def _read_all(self, size):
        """
        读取指定长度的字节
        :param size: 长度
        :return: 读取出的二进制数据
        """
        if isinstance(self.conn, BytesIO):
            # BytesIO 类型 用于演示
            buff = b''
            have = 0
            while have < size:
                chunk = self.conn.read(size - have)
                have += len(chunk)
                buff += chunk
            return buff
        else:
            # socket 类型
            buff = b''
            have = 0
            while have < size:
                chunk = self.conn.recv(size - have)
                have += len(chunk)
                buff += chunk
                # 客户端关闭了连接
                if len(chunk) == 0:
                    raise EOFError()
            return buff

    def args_encode(self, num1, num2=1):
        """
        对调用参数进行编码
        :param num1:  int
        :param num2:  int
        :return: 编码后的二进制数据
        """
        # 处理参数 num1， 4字节整型
        buff = struct.pack("!B", 1)
        buff += struct.pack("!i", num1)

        # 处理参数 num2, 4 字节整型，如为 默认值 1 就不再放到消息中
        if num2 != 1:
            buff += struct.pack("!B", 2)
            buff += struct.pack('!i', num2)

        # 处理消息总长度 4 字节无符号整型
        length = len(buff)

        # 处理方法名 字符串类型
        name = "divide"
        # 字符串长度 4 字节无符号整型
        msg = struct.pack('!I', len(name))
        msg += name.encode()

        msg += struct.pack('!I', length) + buff

        return msg

    def args_decode(self, connection):
        """
        获取调用参数并进行解码
        :param connection: 传输工具对象，如socket对象或者BytesIO对象，从中可以读取消息数据
        :return: 解码后的参数字典
        """
        # 保存到当前对象中，供_read_all方式使用
        self.conn = connection
        param_name_map = {
            1: 'num1',
            2: 'num2',
        }
        param_len_map = {
            1: 4,
            2: 4,
        }
        # 用于保存解码后的参数字典
        args = dict()

        # 读取消息总长度，4字无节符号整数
        buff = self._read_all(4)
        length = struct.unpack('!I', buff)[0]

        # 记录已读取的长度
        have = 0

        # 读取第一个参数，4字节整型
        buff = self._read_all(1)
        have += 1
        param_seq = struct.unpack('!B', buff)[0]
        param_len = param_len_map[param_seq]
        buff = self._read_all(param_len)
        have += param_len
        args[param_name_map[param_seq]] = struct.unpack('!i', buff)[0]

        if have >= length:
            return args

        # 读取第二个参数，4字节整型
        buff = self._read_all(1)
        have += 1
        param_seq = struct.unpack('!B', buff)[0]
        param_len = param_len_map[param_seq]
        buff = self._read_all(param_len)
        have += param_len
        args[param_name_map[param_seq]] = struct.unpack('!i', buff)[0]

        return args

    def result_encode(self, result):
        """
        对调用的结果进行编码
        :param result: float 或 InvalidOperation对象
        :return: 编码后的二进制数据
        """
        if isinstance(result, float):
            # 没有异常，正常执行
            # 处理结果类型，1字节无符号整数
            buff = struct.pack('!B', 1)

            # 处理结果值, 4字节float
            buff += struct.pack('!f', result)
        else:
            # 发生了InvalidOperation异常
            # 处理结果类型，1字节无符号整数
            buff = struct.pack('!B', 2)

            # 处理异常结果值, 字符串
            # 处理字符串长度, 4字节无符号整数
            buff += struct.pack('!I', len(result.message))
            # 处理字符串内容
            buff += result.message.encode()

        return buff

    def result_decode(self, connection):
        """
        对调用结果进行解码
        :param connection: 传输工具对象，如socket对象或者BytesIO对象，从中可以读取消息数据
        :return: 结果数据
        """
        self.conn = connection

        # 取出结果类型, 1字节无符号整数
        buff = self._read_all(1)
        result_type = struct.unpack('!B', buff)[0]
        if result_type == 1:
            # float的结果值， 4字节float
            buff = self._read_all(4)
            result = struct.unpack('!f', buff)[0]
            return result
        else:
            # InvalidOperation对象
            # 取出字符串长度, 4字节无符号整数
            buff = self._read_all(4)
            str_len = struct.unpack('!I', buff)[0]
            buff = self._read_all(str_len)
            message = buff.decode()
            return InvalidOperation(message)


class MethodProtocol(object):
    """解析方法名的实现 """
    def __init__(self, connection):
        self.conn = connection

    def _read_all(self, size):
        """
        读取指定长度的字节
        :param size: 长度
        :return: 读取出的二进制数据
        """
        if isinstance(self.conn, BytesIO):
            # BytesIO类型，用于演示
            buff = b''
            have = 0
            while have < size:
                chunk = self.conn.read(size - have)
                have += len(chunk)
                buff += chunk

            return buff

        else:
            # socket类型
            buff = b''
            have = 0
            while have < size:
                print('have=%d size=%d' % (have, size))
                chunk = self.conn.recv(size - have)
                have += len(chunk)
                buff += chunk

                if len(chunk) == 0:
                    raise EOFError()

            return buff

    def get_method_name(self):
        # 获取方法名
        # 读取字符串长度，4字节无符号整型
        buff = self._read_all(4)
        str_len = struct.unpack('!I', buff)[0]

        # 读取字符串
        buff = self._read_all(str_len)
        name = buff.decode()
        return name


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
