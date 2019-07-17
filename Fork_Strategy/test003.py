import json

# # links = [("Tom","Dick"),("Dick","Harry"),("Tom","Larry"),("Bob","Leroy"),("Bob","Earl")]
# import pprint
# import sys
#
# links = [("Tom", "Dick"), ("Dick", "Harry"), ("Tom", "Larry"), ("Bob", "Leroy"), ("Bob", "Earl"),
#          ("Leroy", "haha"), ("Leroy", "xixi"), ("haha", "hh1"), ("haha", "hh2")
#          ]
# parents, children = zip(*links)
#
# # 提取出全部的父节点和子节点列表
# # print(parents)
# # print(children)
#
# # sys.exit(0)
#
# # root_nodes 是一级节点
# # 所有的一级节点在 parent 里面而不在 children 里面
# # 这一步是为 links 添加 root 节点
# root_nodes = {x for x in parents if x not in children}
# for node in root_nodes:
#     links.append(('Root', node))
#
# # print(links)
# # sys.exit(0)


class Node(object):
    """节点对象 """
    def __init__(self, name: str, desc, parent: str, children: list):
        """
        初始化
        :param name:
        :param desc:
        :param parent:
        :param children:
        """
        self.name = name
        self.desc = desc
        self.parent = parent
        self.children = children

    def get_nodes(self):
        """
        获取该节点下的全部结构字典
        """
        d = dict()
        d['name'] = self.name
        d['desc'] = self.desc
        d['parent'] = self.parent
        children = self.get_children()
        # 递归调用
        if children:
            d['children'] = [child.get_nodes() for child in children]
        return d

    def get_children(self):
        """
        获取该节点下的全部节点对象
        """
        return [n for n in nodes if n.parent == self.name]

    def __repr__(self):
        return self.name


# 原始数据
datas = [
    ["root", "根节点", "root", None],
    ["node1", "一级节点1", "root", "root"],
    ["node2", "一级节点2", "root", "root"],
    ["node11", "二级节点11", "root", "node1"],
    ["node12", "二级节点12", "root", "node1"],
    ["node21", "二级节点21", "root", "node2"],
    ["node22", "二级节点22", "root", "node2"],
]

# 将原始数据转化为节点对象
nodes = []
for data in datas:
    node = Node(data[0], data[1], data[-1], [])
    nodes.append(node)

# 为各个节点对象建立联系
for node in nodes:
    children_names = [data[0] for data in datas if data[-1] == node.name]
    children = [node for node in nodes if node.name in children_names]


root = nodes[0]
print(root)

tree = root.get_nodes()
# print(tree)
print(json.dumps(tree, indent=4))
