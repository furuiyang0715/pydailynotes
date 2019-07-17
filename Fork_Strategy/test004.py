cache = RedisCache("FORKINFO:", encoder=json.dumps, decoder=json.loads)
tree_cache = RedisCache("FORKTREE:", encoder=json.dumps, decoder=json.loads)


@classmethod
def build_tree(cls, strategies, parent):
    # 递归刷新
    def build_tree_recursive(tree: dict, parent: str, strategies: list):
        """
        convert list to tree-like dict
        :param tree:
        :param parent:
        :param strategies:
        :return:
        """
        children = [strategy for strategy in strategies if strategy.get('parent') == parent]
        for child in children:
            tree[child.get("forked_id")] = dict()
            build_tree_recursive(tree[child.get("forked_id")], child.get("forked_id"), strategies)

    tree = dict()
    build_tree_recursive(tree, parent, strategies)
    return tree


@login_require
def get(self, jid):
    forked_infos = self.cache.get(jid)
    if not forked_infos:
        current_app.logger.info("This is first to get forked_infos. No cache.")

        origin = self._check_strategy(jid)
        user_id = request.user.uid
        args = strategyforks_get_parser.parse_args()

        forked_strategies = MongoJStrategies.collection().find({"user_id": user_id, "origin": jid})
        forked_strategies = list(forked_strategies)
        # 将源策略 id 加入forked_strategies 的首位
        forked_strategies.insert(0, origin)

        forked_infos = list()
        for forked_strategy in forked_strategies:
            max_drawdown = None
            annualized_returns = None
            create_time = forked_strategy.get("create_time", None)
            task_names = forked_strategy.get("task_names", [])
            desc = forked_strategy.get("name")
            origin = forked_strategy.get("origin")
            parent = forked_strategy.get("parent")

            if task_names:
                task_id = task_names[-1].split("_")[-1]
                try:
                    task_infos = list(mongo.cx.jztask[task_id].find(
                        {"task_id": task_id}, {"data": 1, "max_drawdown": 1, "_id": 0}))[0]
                except Exception as e:
                    task_infos = dict()
                if task_infos:
                    max_drawdown = task_infos.get("max_drawdown", None)
                    data = task_infos.get("data", {})
                    annualized_returns = data.get("annualized_returns", None)

            forked_infos.append({"forked_id": str(forked_strategy.get("_id")),
                                 "max_drawdown": max_drawdown,
                                 "annualized_returns": annualized_returns,
                                 "create_time": create_time,  # 分支创建时间
                                 "desc": desc,
                                 "origin": origin,
                                 "parent": parent,
                                 })

        nodes = process_datas(forked_infos)
        origin = nodes[0]
        forked_infos = origin.get_nodes()
        self.cache.cache(jid, value=forked_infos)


    return APIResponse(1, {"forked_infos": forked_infos, "git_tree": git_tree}).to_json()


class Node(object):

    nodes = []

    def __init__(self, nodes: list, kwargs):
        """
        初始化
        :param nodes: 树的全部节点对象
        :param kwargs: 当前节点参数
        """

        self.forked_id = kwargs.get("forked_id")
        self.max_drawdown = kwargs.get("max_drawdown")
        self.annualized_returns = kwargs.get("annualized_returns")
        self.create_time = kwargs.get("create_time")
        self.desc = kwargs.get("desc")
        self.origin = kwargs.get("origin")
        self.parent = kwargs.get("parent")
        self.children = kwargs.get("children", [])

    def get_nodes(self):
        """
        获取该节点下的全部结构字典，即建立树状联系
        """
        d = dict()
        d['forked_id'] = self.forked_id
        d['max_drawdown'] = self.max_drawdown
        d['annualized_returns'] = self.annualized_returns
        d['create_time'] = self.create_time
        d['desc'] = self.desc
        d['origin'] = self.origin
        d['parent'] = self.parent
        children = self.get_children()
        if children:
            d['children'] = [child.get_nodes() for child in children]
        return d

    def get_children(self):
        """
        获取该节点下的全部节点对象
        """
        return [n for n in self.nodes if n.parent == self.forked_id]


def process_datas(datas):
    """
    处理原始数据
    :param datas:
    :return:
    """
    # forked_infos.append({"forked_id": str(forked_strategy.get("_id")),
    #  "max_drawdown": max_drawdown,
    #  "annualized_returns": annualized_returns,
    #  "create_time": create_time,  # 分支创建时间
    #  "desc": desc,
    #  "origin": origin,
    #  "parent": parent,
    #
    #  "children": [],
    #  })

    nodes = []
    # 构建节点列表集
    for data in datas:
        node = Node(**data)
        nodes.append(node)

    # 为各个节点对象建立类 nosql 结构的联系
    for node in nodes:
        children_ids = [data["forked_id"] for data in datas if data["parent"] == node.forked_id]
        children = [node for node in nodes if node.forked_id in children_ids]
        node.children.extend(children)

    return nodes
