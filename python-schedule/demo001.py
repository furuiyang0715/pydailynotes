import schedule
import time


def job():
    """
    运行的任务
    :return:
    """
    print("I'm working...")


# 每 10 分钟运行一次
schedule.every(10).minutes.do(job)
# 每小时运行一次
schedule.every().hour.do(job)
# 每天的 10 点半运行一次
schedule.every().day.at("10:30").do(job)
# 每个月运行一次
schedule.every().monday.do(job)
# 每周三的 13：15 运行一次
schedule.every().wednesday.at("13:15").do(job)
# 每分钟的第 17 s 运行
schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
