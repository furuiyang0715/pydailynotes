import sys

import requests as re

base_url = "https://testquant.jingzhuan.cn"
token = "?ts=1552032967116&token=776ed74c99cefe962e8efa59a30ee79a182876ef"

demo_url = "/api/strategyforks/5d0dcc25eba722fbc045c2fa"
url1 = base_url + demo_url + token

all_url = "/api/strategyforks/5d0731472afd8f00184b8f4b"
lookall = base_url + all_url + token

res = re.post(url1)
print(res.text)


# 查看根节点下面的内容
print(re.get(lookall).text)


# print(re.get(url1).text)
#
# # 删除 策略 5d0731472afd8f00184b8f4b 下面的 5d0dc5e49dbbd45edc45c30c 分支
# mydata = {
#     "ids": ("5d0dc5909dbbd45edc45c30b"),
#     "token": "776ed74c99cefe962e8efa59a30ee79a182876ef",
# }
#
# url2 = base_url + post_url
# print(url2)
#
# ret = re.delete(base_url+post_url, data=mydata)
#
# print(ret.text)
#
#
# print(re.get(url1).text)

