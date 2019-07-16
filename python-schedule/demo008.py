import functools
import time

import schedule


# This decorator can be applied to
def with_logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('LOG: Running job "%s"' % func.__name__)
        result = func(*args, **kwargs)
        print('LOG: Job "%s" completed' % func.__name__)
        return result
    return wrapper


@with_logging
def job():
    print('Hello, World.')


schedule.every(3).seconds.do(job)


while 1:
    schedule.run_pending()
    time.sleep(1)
