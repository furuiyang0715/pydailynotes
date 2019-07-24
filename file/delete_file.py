import os
import shutil

to_delete_path = os.path.join(os.getcwd(), "哈哈哈哈哈")

ret = shutil.rmtree(to_delete_path, ignore_errors=True)

print(ret)