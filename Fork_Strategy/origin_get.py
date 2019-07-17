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
    git_tree = self.tree_cache.get(jid)

    if not forked_infos:
        current_app.logger.info("This is first to get forked_infos. No cache.")
        origin = self._check_strategy(jid)
        user_id = request.user.uid
        args = strategyforks_get_parser.parse_args()
        node_type = args.get("node")

        if node_type == "all":
            if origin.get("parent"):
                message = f"暂时不支持在源策略节点 {origin.get('parent')} 之外的刷新请求"
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
        # 将forked_infos按照时间排序
        forked_infos = sorted(forked_infos, key=lambda item: item["create_time"])
        # current_app.logger.info(f"{forked_infos}")
        self.cache.cache(jid, value=forked_infos)
        if not git_tree:
            current_app.logger.info("This is first to get git tree. No cache.")
            git_tree = self.build_tree(forked_infos, jid)
            self.tree_cache.cache(jid, value=git_tree)
    return APIResponse(1, {"forked_infos": forked_infos, "git_tree": git_tree}).to_json()