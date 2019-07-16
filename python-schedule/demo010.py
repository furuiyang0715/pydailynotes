import time

import schedule


def greet(name):
    print('Hello', name)


schedule.every(2).seconds.do(greet, name='Alice')
schedule.every(4).seconds.do(greet, name='Bob')

while True:
    schedule.run_pending()
    time.sleep(3)
