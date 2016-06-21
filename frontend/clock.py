from apscheduler.schedulers.blocking import BlockingScheduler
import random

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every one min')
    with open("companies.txt", 'w') as fw:
        random_num = str(random.randint(1, 100))
        fw.write(random_num)
        print("written to file")

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()
