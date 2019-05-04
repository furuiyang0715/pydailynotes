import pprint
import sys


def property_repr(inst):
    # return pformat(properties(inst))
    # 包含当前类的名称以及对应的属性值 同时剔除可能被废弃的属性
    return "%s(%s)" % (inst.__class__.__name__, properties(inst))
    # 前面是类名字 后面是属性值字典


def properties(inst):
    result = {}
    for cls in inst.__class__.mro():
        # 当前类的父类 多继承的 mro
        # 找出被废弃的属性
        abandon_properties = getattr(cls, '__abandon_properties__', [])
        # sys.exit(0)
        for varname in iter_properties_of_class(cls):
            if varname[0] == "_":
                continue
            if varname in abandon_properties:
                # 如果 设置了 __abandon_properties__ 属性，则过滤其中的property，不输出相关内容
                continue
            # FIXME 这里getattr在iter_properties_of_class中掉用过了，性能比较差，可以优化
            tmp = getattr(inst, varname)
            if varname == "positions":
                tmp = list(tmp.keys())
            if hasattr(tmp, '__simple_object__'):
                result[varname] = tmp.__simple_object__()
            else:
                result[varname] = tmp
    return result


def iter_properties_of_class(cls):
    for varname in vars(cls):
        value = getattr(cls, varname)
        # 判断是否是一个属性函数
        if isinstance(value, property):
            yield varname


# 定义一个类
class People(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def run(self):
        return "I am running..."

    @property
    def bigname(self):
        return self.name + str(self.age)


pp = People("ruiyang", 25)

# cls = pp.__class__  # <class '__main__.People'>

# print(cls)


class Stu(People):
    pass


cls = Stu("ruiyang", 25).__class__

print(cls.__name__)  # Stu


# print(Stu.__mro__)
# 打印出其继承树 (<class '__main__.Stu'>, <class '__main__.People'>, <class 'object'>)

# vars 内置方法，返回对象的object的属性和属性值的字典对象
# 有关 vars() globals() 以及locales() 之间的区别：
# https://www.techforgeek.info/vars_globals_locals.html
# print(pprint.pformat(vars(cls)))
"""
mappingproxy({'__dict__': <attribute '__dict__' of 'People' objects>,
              '__doc__': None,
              '__init__': <function People.__init__ at 0x105272bf8>,
              '__module__': '__main__',
              '__weakref__': <attribute '__weakref__' of 'People' objects>,
              'run': <function People.run at 0x105272c80>})

"""

# for i in iter_properties_of_class(cls):
#     print(i)  # bigname

print(properties(Stu("ruiyang", 25)))  # {'bigname': 'ruiyang25'}


