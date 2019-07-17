
class InvalidOperation(Exception):
    """
    自定义非法操作异常
    """
    def __init__(self, message=None):
        self.message = message or "Invalid operation."


def divide(num1, num2=1):
    """
    除法
    :param num1:  int
    :param num2:  int 默认为 1
    :return:  float 商 或者 无效的异常值
    """
    if num2 == 0:
        raise InvalidOperation()
    val = num1 / num2
    return val


# 尝试在本地调用
try:
    val = divide(200, 100)
except InvalidOperation as e:
    print(e.message)
else:
    print(val)
    # print(type(val))



