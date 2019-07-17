class JStrategyForks(Resource, JStrategyMixin):
    forked_strategies_obj = None

    def forked_strategies(self, jid):
        # 这里是没有包含源策略节点
        if self.forked_strategies_obj is not None:
            return self.forked_strategies_obj

        user_id = request.user.uid
        forked_strategies = MongoJStrategies.collection().find({"user_id": user_id, "origin": jid})
        self.forked_strategies_obj = [self._check_strategy(str(strategy.get("_id"))) for strategy in forked_strategies]

    @classmethod
    def build_tree(cls, strategies, parent):

        def build_tree_recursive(_tree, _parent, _strategies, _related_strategies_list):
            # find children
            children = [strategy for strategy in _strategies if strategy.get('parent') == _parent]

            _related_strategies_list.extend([c.get("id") for c in children])

            # build a subtree for each child
            for child in children:
                # start new subtree
                _tree[child.get("id")] = dict()

                # call recursively to build a subtree for current node
                build_tree_recursive(_tree[child.get("id")], child.get("id"), _strategies, _related_strategies_list)

        related_strategies_list = list()
        tree = dict()
        build_tree_recursive(tree, parent, strategies, related_strategies_list)
        return tree, related_strategies_list

    def gen_tree_info(self, jid):
        """
        抽取获取节点 info 的方法
        :param jid: 被抽取 info 的节点 id
        :return:
        """
        strategy = self._check_strategy(jid)
        # 判断 "all" or "child"
        origin_jid = strategy.get("origin") or jid
        self.forked_strategies(origin_jid)
        tree_info, related_strategies_list = self.build_tree(self.forked_strategies_obj, jid)
        return tree_info, related_strategies_list

    @login_require
    def get(self, jid):
        """
        以当前节点为基准的结构信息
        :param jid:
        :return:
        """
        # args = strategyforks_get_parser.parse_args()
        # node_type = args.get("node")

        try:
            tree_info, related_strategies_list = self.gen_tree_info(jid)
            # if node_type == "all":
            #     current_strategy = self._check_strategy(jid)
            #     # current_strategy['parent'] = None
            #     self.forked_strategies(jid)
            #     tree_info, related_strategies_list = self.build_tree(self.forked_strategies_obj, jid)
            # else:
            #     # 非源策略
            #     current_strategy = self._check_strategy(jid)
            #     origin_jid = current_strategy.get("origin")
            #     self.forked_strategies(origin_jid)
            #     tree_info, related_strategies_list = self.build_tree(self.forked_strategies_obj, jid)
        except APIError as e:
            current_app.logger.error(f"[JStrategyForks] get 查询 fork 节点数据失败. jid={jid}, error={e}")
            return APIResponse.error(APIResponse.CODE_OPERATION_FAILED,
                                     message="操作失败，fork 节点查询有误")
        res = {
            "tree_info": tree_info,
            "related_strategies_list": related_strategies_list
        }
        return APIResponse(1, res).to_json()

    @login_require
    def post(self, jid):
        """
        为策略 fork 出新分支
        :param jid:
        :return:
        """
        jstrategy = self._check_strategy(jid)

        # 只有fork过的接口存在origin和parent两个字段
        # origin 的赋值判断：
        # (1) 如果当前jstrategy存在origin字段，说明其不是原始节点，保持origin不变
        # (2) 如果当前jstrategy不存在origin字段，说明是原始节点，将origin赋值为当前jid
        origin = jstrategy.get("origin")
        if not origin:
            jstrategy["origin"] = jid

        jstrategy["parent"] = jid

        timestamp = int(time.time())
        jstrategy.update({
            'modified_time': timestamp,
            'create_time': timestamp,
            'task_names': []
        })

        forked_strategy = MongoJStrategies.create_new(**jstrategy)
        user = request.user
        current_app.logger.info(
            f"[PostJStrategyForks] new user={user}, forked_strategy={forked_strategy}")
        return APIResponse(1, {"forked_id": forked_strategy}).to_json()

    @login_require
    def delete(self, jid):
        """
        删除一个或者多个策略分支
        :param jid:
        :param ids: 要删除的策略分支节点ids eg.ids=(1,2,3）
        :return:
        """
        self._check_strategy(jid)
        args = strategyforks_delete_parser.parse_args()
        ids = args.get("ids")
        id_list = ids.strip("()").split(",")
        if id_list:
            try:
                for id in id_list:
                    _, related_strategies_list = self.gen_tree_info(id)
                    # 删除关联节点
                    if related_strategies_list:
                        related_strategies_list = [bson.ObjectId(id) for id in related_strategies_list]
                        ret = MongoJStrategy.collection().delete_many({"_id": {"$in": related_strategies_list}})
                        print(ret.deleted_count)
                        if ret.deleted_count == 0:
                            raise FileNotFoundError("找不到源策略 {} 对应应删除的 forked 策略id".format(id))

                    # 删除当前节点
                    id = self._check_strategy(id).get("id")
                    res = MongoJStrategy.delete(id)
                    if res.deleted_count == 0:
                        raise FileNotFoundError("找不到应删除的策略id：{}".format(id))
            except Exception:
                current_app.logger.info(f"[DeleteForkedStrategy] failed.ids={ids}, user={request.user}")
                return APIResponse(3).to_json()

        current_app.logger.info(
            f"[DeleteForkedStrategy] deleted. ids={ids}, user={request.user}")
        return APIResponse(1).to_json()