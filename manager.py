from jobs import write_cat_to_file
from apscheduler.schedulers.blocking import BlockingScheduler


scheduler = BlockingScheduler()
if __name__ == '__main__':
    scheduler.add_job(func=write_cat_to_file, trigger='interval', seconds=60)
    scheduler.start()
