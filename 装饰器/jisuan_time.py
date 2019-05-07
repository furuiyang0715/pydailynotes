import time


def log_method_time_usage(func):
    def wrapped(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        # system_log.info(f"[TimeUsage] {func.__module__}.{func.__name__} usage: {time.time()-start}")
        dt = time.time()-start
        if dt > 0.1:
            print(f"[TimeUsage] {func.__module__}.{func.__name__} usage: {dt}")
        return result
    return wrapped


@log_method_time_usage
def func(num):
    for i in range(num):
        print("hello")
        time.sleep(3)


if __name__ == "__main__":
    func(3)
