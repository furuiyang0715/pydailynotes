# 给去除了背景的图像添加各色背景

from PIL import Image

# 输入已经去除背景的图像
im = Image.open('/Users/furuiyang/mygit/pydailynotes/image/pic/lixian.jpeg_no_bg.png')
x, y = im.size

try:
    # 使用白色来填充背景
    # (alpha band as paste mask).
    p = Image.new('RGBA', im.size, (255, 0, 255))
    p.paste(im, (0, 0, x, y), im)
    # 保存转换后的退图像
    p.save('/Users/furuiyang/mygit/pydailynotes/image/pic/lixian.jpeg_new_bg.png')
except:
    pass
