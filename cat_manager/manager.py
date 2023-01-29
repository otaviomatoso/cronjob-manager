from cat_manager.jobs import write_cat_to_file
from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler()
scheduler.add_job(func=write_cat_to_file, trigger='interval', seconds=60)
scheduler.start()
