# 使用 Python struct 模块

# struct.pack(格式, 数据)
import struct

a = struct.pack('!I', 6)

print(a)

# unpack 返回的是一个元组
ret = struct.unpack("!I", a)

print(ret)


