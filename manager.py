from jobs import Cat
from apscheduler.schedulers.blocking import BlockingScheduler


scheduler = BlockingScheduler()
scheduler.add_job(func=Cat.write_to_file_job, trigger='interval', seconds=5)
scheduler.start()
