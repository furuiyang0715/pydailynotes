import os
import shutil

to_delete_path = os.path.join(os.getcwd(), "哈哈哈哈哈")

# 循环删除文件夹以及文件夹中的内容
ret = shutil.rmtree(to_delete_path, ignore_errors=True)

print(ret)