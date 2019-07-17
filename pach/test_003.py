from bs4 import BeautifulSoup

soup = BeautifulSoup('<p>Hello</p>', 'lxml')
# print(soup.p.string)


html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
soup = BeautifulSoup(html, 'lxml')
# prettify() 这个方法可以把要解析的字符串以标准的缩进格式输出
# print(soup.prettify())
# 输出了 HTML 中 title 节点的文本内容
# print(soup.title.string)


html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
soup = BeautifulSoup(html, 'lxml')
print(soup.title)
#  bs4.element.Tag 类型，这是 BeautifulSoup 中的一个重要的数据结构，经过选择器选择之后，
#  选择结果都是这种 Tag 类型，它具有一些属性比如 string 属性，调用 Tag 的 string 属性，就可以得到节点的文本内容了
print(type(soup.title))
print(soup.title.string)
print(soup.head)
# 当有多个节点时，这种选择方式只会选择到第一个匹配的节点，其他的后面的节点都会忽略
print(soup.p)

# 利用 name 属性来获取节点的名称
print(soup.title.name)
print(soup.p.attrs)
print(soup.p.attrs['name'])

print(soup.p['name'])
print(soup.p['class'])

print(soup.p.string)

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
"""
soup = BeautifulSoup(html, 'lxml')
print(soup.head.title)
print(type(soup.head.title))
print(soup.head.title.string)

html = """
<html>
    <head>
        <title>The Dormouse's story</title>
    </head>
    <body>
        <p class="story">
            Once upon a time there were three little sisters; and their names were
            <a href="http://example.com/elsie" class="sister" id="link1">
                <span>Elsie</span>
            </a>
            <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> 
            and
            <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
            and they lived at the bottom of a well.
        </p>
        <p class="story">...</p>
"""

soup = BeautifulSoup(html, 'lxml')
print(soup.p.contents)

soup = BeautifulSoup(html, 'lxml')
print(soup.p.children)
for i, child in enumerate(soup.p.children):
    print(i, child)


print("*"*100)
print(soup.p.descendants)
for i, child in enumerate(soup.p.descendants):
    print(i, child)

