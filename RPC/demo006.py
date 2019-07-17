# from services import ClientStub
# from services import Channel
# from services import InvalidOperation
import time

from RPC.demo001 import InvalidOperation
from RPC.demo004_tcp_server import Channel
from RPC.demo005 import ClientStub

channel = Channel('127.0.0.1', 8888)
stub = ClientStub(channel)

for i in range(20):
    try:
        val = stub.divide(i*100, 10)
    except InvalidOperation as e:
        print(e.message)
    else:
        print(val)
    time.sleep(1)
