import os
import pprint
import sys

import etcd

env = os.environ.get
QUANT_ENV = env("QUANT_ENV", "root")
ETCD_HOST = env("ETCD_HOST", "127.0.0.1")
ETCD_PORT = int(env("ETCD_PORT", 2379))
QUANT_TYPE = env("QUANT_TYPE", "backtest")
this = sys.modules[__name__]


class EtcdConfig(object):

    def __init__(self, host: str = None, port: int = None, **kwargs):
        """
        :param host: etcd server host
        :param port: etcd server port
        :param kwargs:
            srv_domain (str): Domain to search the SRV record for cluster autodiscovery.

            version_prefix (str): Url or version prefix in etcd url (default=/v2).

            read_timeout (int):  max seconds to wait for a read.

            allow_redirect (bool): allow the client to connect to other nodes.

            protocol (str):  Protocol used to connect to etcd.

            cert (mixed):   If a string, the whole ssl client certificate;
                            if a tuple, the cert and key file names.

            ca_cert (str): The ca certificate. If pressent it will enable
                           validation.

            username (str): username for etcd authentication.

            password (str): password for etcd authentication.

            allow_reconnect (bool): allow the client to reconnect to another
                                    etcd server in the cluster in the case the
                                    default one does not respond.

            use_proxies (bool): we are using a list of proxies to which we connect,
                                 and don't want to connect to the original etcd cluster.

            expected_cluster_id (str): If a string, recorded as the expected
                                       UUID of the cluster (rather than
                                       learning it from the first request),
                                       reads will raise EtcdClusterIdChanged
                                       if they receive a response with a
                                       different cluster ID.
            per_host_pool_size (int): specifies maximum number of connections to pool
                                      by host. By default this will use up to 10
                                      connections.
            lock_prefix (str): Set the key prefix at etcd when client to lock object.
                                      By default this will be use /_locks.
        """
        self._etcd = etcd.Client(host=host, port=port, **kwargs)

    def get_config(self, dir: str) -> dict or None:
        """
        returns all key / value mappings recursivly coresponding to key dir
        if the dir is not existed return None
        if value is not a dir returns the value itself
        :param dir: key of a dir
        :return:
        """
        try:
            d = self._etcd.get(dir)
        except etcd.EtcdKeyNotFound:
            return None
        if not d.dir:
            return d.value

        cfg = {}
        for chld in d.children:
            local = chld.key.split("/")[-1]
            cfg[local] = self.get_config(chld.key)

        return cfg

    def get_value(self, key: str) -> str:
        """
        get_value returns the value of a key
        :param key:
        :return:
        """
        return self._etcd.get(key)

    def store(self, key: str, value: str or dict):
        """
        stores value into etcd with key.
        the value must be str or dict
        :param key:
        :param value:
        :return:
        """
        if isinstance(value, dict):
            for k, v in value.items():
                new_key = "/".join([key, k])
                self.store(new_key, v)
        else:
            self._etcd.set(key, value)


# client = EtcdConfig(host=ETCD_HOST, port=ETCD_PORT)
client = EtcdConfig(host="127.0.0.1", port=2379, username="root", password="123465")


def _p(key: str) -> str:
    return "/".join(["jq", QUANT_ENV, key])


def bool_number(v: str):
    if isinstance(v, str):
        vl = v.lower()
    else:
        vl = str(v).lower()
    if vl == "true":
        return True
    elif vl == "false":
        return False
    if vl.isnumeric():
        return int(v)
    try:
        return float(v)
    except (ValueError, TypeError):
        return v


def type_it(d: dict):
    keys = d.keys()
    for k in keys:
        v = d[k]
        if isinstance(v, dict):
            type_it(v)
        else:
            d[k] = bool_number(v)


def get_config():
    envs = client.get_config(_p(f"quant/{QUANT_TYPE}/env"))
    for k, v in envs.items():
        setattr(this, k, v)
    ft = client.get_config(_p("future"))
    type_it(ft)
    setattr(this, "SERVICE_FUTURE", ft)

    idx = client.get_config(_p("index"))
    type_it(idx)
    setattr(this, "SERVICE_INDEX", idx)

    mq = client.get_config(_p("mq"))
    type_it(mq)
    setattr(this, "SERVICE_MQ", mq)

    oss = client.get_config(_p("oss"))
    type_it(oss)
    setattr(this, "SERVICE_OSS", oss)

    qu = client.get_config(_p("quantuser"))
    type_it(qu)
    setattr(this, "SERVICE_QUANTUSER", qu)

    quote = client.get_config(_p("quote"))
    type_it(quote)
    setattr(this, "SERVICE_QUOTE", quote)

    rds = client.get_config(_p("redis"))
    type_it(rds)
    setattr(this, "SERVICE_REDIS", rds)

    st = client.get_config(_p("stock_trade"))
    type_it(st)
    setattr(this, "SERVICE_STOCK_TRADE", st)

    tae = client.get_config(_p("tae"))
    type_it(tae)
    setattr(this, "SERVICE_TAE", tae)


if __name__ == "__main__":
    print("into")

    # 查看 back 中的配置
    # print(pprint.pformat(client.get_config("/jq/test/backend")))
    # print(pprint.pformat(client.get_config("jq/furuiyang/quant/backtest/env")))
    # print(pprint.pformat(client.get_config("jq/yuxuyang/quant/backtest/env")))

    # 查看下 redis 的配置
    # print(pprint.pformat(client.get_config("/jq/test/redis")))

    # 获取配置
    # get_config()

    infos = client.get_config("jq/furuiyang/")
    client.store("/jq/yuxuyang/", infos)








