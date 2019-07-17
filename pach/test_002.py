# python 解析库 lxml
from lxml import etree

text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
     </ul>
 </div>
'''
# 构建一个 html 对象
html = etree.HTML(text)
# print(html)

# 将其转换为 bytes 对象
result = etree.tostring(html)

# 进行 bytes 到 str 的转换
# print(result.decode('utf-8'))
# print(type(result.decode('utf-8')))


# 也可以直接读取文本进行解析
html = etree.parse('./test.html', etree.HTMLParser())
result = etree.tostring(html)
# print(result.decode('utf-8'))

# 如果我们要选取所有的节点 可以这样进行
html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//*')
# print(result)

# 如果我们只想获取其中的某一种节点 例如 li
html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//li')
# print(result)
# print(result[0])


# 获取子节点以及孙子节点
html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//li/a')
# print(result)

# // 获取所有的孙子节点 / 获取直接的子节点
html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//ul//a')
# print(result)

# 首先选中 href 是 link4.html 的 a 节点，然后再获取其父节点，然后再获取其 class 属性
html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//a[@href="link4.html"]/../@class')
# print(result)

# 同时我们也可以通过 parent:: 来获取父节点
html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//a[@href="link4.html"]/parent::*/@class')
# print(result)


# 属性匹配  要选取 class 为 item-1 的 li 节点
html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//li[@class="item-0"]')
# print(result)

# 文本获取: 用 XPath 中的 text() 方法可以获取节点中的文本
html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//li[@class="item-0"]/text()')
# print(result)


# 先到 a 节点下面再获取文本
html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//li[@class="item-0"]/a/text()')
print(result)
