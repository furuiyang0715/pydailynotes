from removebg import RemoveBg
import os

# 参数填入 api key 以及批处理的日志文件位置
rmbg = RemoveBg("u3NcF5HuRAbKow7x9v7BJbfS", "./error.log")

# 批处理图片的存放位置
path = os.path.join(os.getcwd(), "pic")

for pic in os.listdir(path):
    rmbg.remove_background_from_img_file(os.path.join(path, pic))
