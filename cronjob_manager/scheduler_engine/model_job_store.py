from apscheduler.job import Job as Job
from apscheduler.jobstores.base import BaseJobStore, JobLookupError
from cronjobs.models.job import Job as JobModel
from django.core.exceptions import ObjectDoesNotExist
from typing import List
import pickle
import pytz


class ModelJobStore(BaseJobStore):

    def start(self, *args, **kwargs):
        super(ModelJobStore, self).start(*args, **kwargs)

    def lookup_job(self, job_id):
        return JobModel.objects.get(u_id=job_id)

    def get_due_jobs(self, now) -> List[Job]:
        now_utc = now.astimezone(pytz.utc)
        due_jobs = JobModel.objects.filter(next_run_time__lte=now_utc)
        return [self._deserialize_job(job) for job in due_jobs]

    def get_next_run_time(self):
        if next_job := JobModel.objects.all().order_by('next_run_time').first():
            return next_job.next_run_time

    def get_all_jobs(self):
        all_jobs = JobModel.objects.all()
        return [self._deserialize_job(job) for job in all_jobs]

    def add_job(self, job: Job):
        serialized_job = self._serialize_job(job)
        serialized_job.save()

    def remove_job(self, job_id):
        try:
            job = JobModel.objects.get(u_id=job_id)
            job.delete()
        except JobModel.DoesNotExist:
            raise JobLookupError("Job not found")

    def update_job(self, job):
        try:
            job_model = JobModel.objects.get(u_id=job.id)
            job_model.next_run_time = job.next_run_time.astimezone(pytz.utc)
            # job_model.job_state = self._pickle(job.__getstate__())
            job_model.save()
        except JobModel.DoesNotExist:
            raise JobLookupError("Job not found")

    def remove_all_jobs(self):
        try:
            JobModel.objects.all().delete()
        except ObjectDoesNotExist:
            pass

    def _serialize_job(self, job: Job) -> JobModel:
        serialized_job = JobModel(u_id=job.id,
                                  key=job.kwargs.get('key', '').value,
                                  next_run_time=job.next_run_time.astimezone(pytz.utc),
                                  job_state=self._pickle(job.__getstate__()))
        return serialized_job

    def _deserialize_job(self, serialized_job: JobModel) -> Job:
        job_state = serialized_job.job_state
        job_state = self._unpickle(job_state)
        job_state['jobstore'] = self
        job = Job.__new__(Job)
        job.__setstate__(job_state)
        job._scheduler = self._scheduler
        job._jobstore_alias = self._alias
        return job

    @staticmethod
    def _pickle(obj):
        return pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def _unpickle(obj):
        return pickle.loads(obj)
