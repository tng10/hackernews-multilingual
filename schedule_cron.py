from crontab import CronTab
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))

my_cron = CronTab(user='root')
job = my_cron.new(command='python %s/drop_cache.py' % dir_path)
job.minute.every(10)

my_cron.write()
