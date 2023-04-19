from apscheduler.schedulers.background import BackgroundScheduler
from enums import JobTypes
from scheduler_engine.model_job_store import ModelJobStore


scheduler = BackgroundScheduler()
scheduler.add_jobstore(jobstore=ModelJobStore())
scheduler.add_job(func='cat_manager.jobs.cat:write_cat_to_file', trigger='interval', seconds=10,
                  kwargs={'key': JobTypes.CAT, 'file_name': 'cat_file.txt'},
                  misfire_grace_time=None, coalesce=True, replace_existing=True)
scheduler.start()
