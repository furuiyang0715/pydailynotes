# 通过构造一个生成器不断地生成新的 id
def id_gen(start=1):
    i = start
    while True:
        yield i
        i += 1


gener = id_gen(44)
print(gener)
for i in range(10):
    print(next(gener))
