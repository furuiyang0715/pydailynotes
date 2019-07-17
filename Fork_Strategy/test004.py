@login_require
def get(self, jid):
    """
    获取当前策略下的forked strategies
    node_type = "all"    针对原始节点
    node_type = "child"  针对中间节点
    :param jid:
    :return:
    """
    forked_infos = self.cache.get(jid)
    # git_tree = self.tree_cache.get(jid)

    if not forked_infos:
        current_app.logger.info("This is first to get forked_infos. No cache.")
        origin = self._check_strategy(jid)
        user_id = request.user.uid
        args = strategyforks_get_parser.parse_args()
        node_type = args.get("node")

        if node_type == "all":
            if origin.get("parent"):
                message = f"暂时不支持在源策略节点 {origin.get('parent')} 之外的刷新请求"  # FIXME
                return APIResponse(7, message).to_json()

            forked_strategies = MongoJStrategies.collection().find({"user_id": user_id, "origin": jid})
        else:
            forked_strategies = MongoJStrategies.collection().find({"user_id": user_id, "parent": jid})

        forked_strategies = list(forked_strategies)
        # 为了前端展示，将源策略 id 加入forked_strategies
        forked_strategies.append(origin)
        # current_app.logger.info(f"{forked_strategies}")

        forked_infos = list()
        for forked_strategy in forked_strategies:
            max_drawdown = None
            annualized_returns = None
            create_time = forked_strategy.get("create_time", None)
            task_names = forked_strategy.get("task_names", [])
            desc = forked_strategy.get("name")
            origin = forked_strategy.get("origin")
            parent = forked_strategy.get("parent")

            if task_names:  # 表明该forked出来的策略有进行过回测
                # 查询出最近的一个 task 的收益率和最大回撤的值
                # task_names 是一个 push 的列表结构 取出最后一个值 即为最新值 :
                # MongoJStrategy.update(id, {"$push": {"task_names": task_name}})
                task_id = task_names[-1].split("_")[-1]
                try:
                    task_infos = list(mongo.cx.jztask[task_id].find(
                        {"task_id": task_id}, {"data": 1, "max_drawdown": 1, "_id": 0}))[0]
                except Exception as e:
                    task_infos = dict()
                if task_infos:
                    # current_app.logger.info(f"{task_infos}")
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
            # current_app.logger.info(f"{forked_infos}")
            # # 将forked_infos按照时间排序
            # forked_infos = sorted(forked_infos, key=lambda item: item["create_time"])
            # current_app.logger.info(f"{forked_infos}")
            self.cache.cache(jid, value=forked_infos)
        # if not git_tree:
        #     current_app.logger.info("This is first to get git tree. No cache.")
        #     git_tree = self.build_tree(forked_infos, jid)
        #     self.tree_cache.cache(jid, value=git_tree)
    return APIResponse(1, {"forked_infos": forked_infos, "git_tree": git_tree}).to_json()


class Node(object):

    # nodes = []

    def __init__(self, nodes: list, kwargs):
        """
        初始化
        :param nodes: 树的全部节点对象
        :param kwargs: 当前节点参数
        """

        self.nodes = nodes

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
        获取该节点下的全部结构字典
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
        # 递归调用
        if children:
            d['children'] = [child.get_nodes() for child in children]
        return d

    def get_children(self):
        """
        获取该节点下的全部节点对象
        """
        return [n for n in self.nodes if n.parent == self.forked_id]

    # def _process_datas(self, datas):
    #     """
    #     处理原始数据
    #     :param datas:
    #     :return:
    #     """
    #
    #     # forked_infos.append({"forked_id": str(forked_strategy.get("_id")),
    #     #  "max_drawdown": max_drawdown,
    #     #  "annualized_returns": annualized_returns,
    #     #  "create_time": create_time,  # 分支创建时间
    #     #  "desc": desc,
    #     #  "origin": origin,
    #     #  "parent": parent,
    #     #
    #     #  "children": [],
    #     #  })
    #
    #     # 构建节点列表集
    #     for data in datas:
    #         node = Node(**data)
    #         self.nodes.append(node)
    #
    #     # 为各个节点对象建立联系
    #     for node in self.nodes:
    #         children_ids = [data["forked_id"] for data in datas if data["parent"] == node.forked_id]
    #         children = [node for node in self.nodes if node.forked_id in children_ids]
    #         node.children.extend(children)

    # def __repr__(self):
    #     # just for test
    #     return self.forked_id


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

    # 为各个节点对象建立联系
    for node in nodes:
        children_ids = [data["forked_id"] for data in datas if data["parent"] == node.forked_id]
        children = [node for node in nodes if node.forked_id in children_ids]
        node.children.extend(children)

    return nodes
