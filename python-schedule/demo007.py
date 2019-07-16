import random
import time

import schedule


def greet(name):
    print('Hello {}'.format(name))


schedule.every(4).seconds.do(greet, 'Andrea').tag('daily-tasks', 'friend')
schedule.every(4).seconds.do(greet, 'John').tag('hourly-tasks', 'friend')
schedule.every(3).seconds.do(greet, 'Monica').tag('hourly-tasks', 'customer')
schedule.every(2).seconds.do(greet, 'Derek').tag('daily-tasks', 'guest')


while True:
    schedule.run_pending()
    n = random.randint(1, 5)
    print(n)
    if n == 3:
        schedule.clear('daily-tasks')
    time.sleep(10)
