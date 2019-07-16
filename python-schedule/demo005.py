import functools

import schedule


def catch_exceptions(cancel_on_failure=False):
    """
    捕获异常处理程序
    :param cancel_on_failure: 决定在异常出现时是否对程序进行中断
    :return:
    """
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except:
                import traceback
                print(traceback.format_exc())
                if cancel_on_failure:
                    return schedule.CancelJob
        return wrapper
    return catch_exceptions_decorator


@catch_exceptions(cancel_on_failure=True)
def bad_task():
    return 1 / 0


schedule.every(5).seconds.do(bad_task)

while True:
    schedule.run_pending()
