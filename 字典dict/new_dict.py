import collections
import pprint

import six


class RqAttrDict(object):
    # 一个重写的字典类

    def __init__(self, d=None):
        # 其属性字典全部由源字典获取
        self.__dict__ = d if d is not None else dict()

        for k, v in list(six.iteritems(self.__dict__)):
            if isinstance(v, dict):
                self.__dict__[k] = RqAttrDict(v)

    def __repr__(self):
        # 更改其输出行为
        return pprint.pformat(self.__dict__)

    def __iter__(self):
        # 具有字典的迭代行为
        return self.__dict__.__iter__()

    def update(self, other):
        RqAttrDict._update_dict_recursive(self, other)

    def items(self):
        # 主要是生成一个字典迭代对象 类似于生成器？？
        return six.iteritems(self.__dict__)

    iteritems = items

    @staticmethod
    def _update_dict_recursive(target, other):
        # 将 other 合并到 target
        if isinstance(other, RqAttrDict):
            other = other.__dict__
        if isinstance(target, RqAttrDict):
            target = target.__dict__

        for k, v in six.iteritems(other):
            # 递归
            if isinstance(v, collections.Mapping):
                r = RqAttrDict._update_dict_recursive(target.get(k, {}), v)
                target[k] = r
            else:
                target[k] = other[k]
        return target

    def convert_to_dict(self):
        # 转化为普通的字典
        result_dict = {}
        for k, v in list(six.iteritems(self.__dict__)):
            if isinstance(v, RqAttrDict):
                v = v.convert_to_dict()
            result_dict[k] = v
        return result_dict


if __name__ == "__main__":
    dd = {
        "furuiyang": {
            "name": {"name1": "ruiyang", "name2": "furuiyang", "name3": "feiyangyang"},
            "age": 25,
            "height": 161,
            "weight": 120
        },
        "yaokailun": {
            "name": {"name1": "kailun", "name2": "xiaopangzi"}
        }
    }
    new = RqAttrDict(dd)
    # print(dd)
    # print(new)

    # print(list(dd.items()))
    # print(six.iteritems(dd))
    # print(new.items())
