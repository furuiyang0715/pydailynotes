import functools
import time

import schedule


def with_logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t1 = time.time()  # 本次执行的时间点
        print('LOG: Running job "%s"' % func.__name__)
        result = func(*args, **kwargs)
        print('LOG: Job "%s" completed' % func.__name__)
        print(time.time() - t1)  # 可以看做是上一次执行的时间

        return result
    return wrapper


@with_logging
def my_job():
    # This job will execute every 5 to 10 seconds.
    print('Foo')


schedule.every(5).to(10).seconds.do(my_job)


while True:
    schedule.run_pending()
    time.sleep(3)
