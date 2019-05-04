def safe_round(value, ndigits=3):
    # 保留指定位数的小数 默认通过四舍五入保留三位小数
    if isinstance(value, float):
        return round(value, ndigits)
    return value


if __name__ == "__main__":
    value = 3.1415926
    print(safe_round(value, 4))

