from apscheduler.job import Job as Job
from apscheduler.jobstores.base import BaseJobStore, JobLookupError
from cronjobs.models.job import Job as JobModel
from django.core.exceptions import ObjectDoesNotExist
from enums import JobStatus
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
        due_jobs = JobModel.objects.filter(next_run_time__lte=now_utc, status=JobStatus.SCHEDULED.value)
        return [self._create_job_from_model(job) for job in due_jobs]

    def get_next_run_time(self):
        if next_job := JobModel.objects.filter(status=JobStatus.SCHEDULED.value).order_by('next_run_time').first():
            return next_job.next_run_time

    def get_all_jobs(self):
        all_jobs = JobModel.objects.all()
        return [self._create_job_from_model(job) for job in all_jobs]

    def add_job(self, job: Job):
        job_model = self._create_model_from_job(job)
        job_model.save()
        model_id = job_model.id
        job.kwargs['model_id'] = model_id
        job_model.job_state = self._pickle(job.__getstate__())
        job_model.save()

    def remove_job(self, job_id):
        try:
            job = JobModel.objects.get(u_id=job_id)
            job.status = JobStatus.DONE.value
            job.save()
        except JobModel.DoesNotExist:
            raise JobLookupError("Job not found")

    def update_job(self, job):
        try:
            job_model = JobModel.objects.get(u_id=job.id, status=JobStatus.SCHEDULED.value)
            job_model.status = JobStatus.DONE.value
            job_model.save()
            self.add_job(job)
        except JobModel.DoesNotExist:
            raise JobLookupError("Job not found")

    def remove_all_jobs(self):
        try:
            JobModel.objects.all().delete()
        except ObjectDoesNotExist:
            pass

    def _create_model_from_job(self, job: Job) -> JobModel:
        serialized_job = JobModel(u_id=job.id,
                                  key=job.kwargs.get('key', '').value,
                                  next_run_time=job.next_run_time.astimezone(pytz.utc),
                                  job_state=self._pickle(job.__getstate__()),
                                  status=JobStatus.SCHEDULED.value)
        return serialized_job

    def _create_job_from_model(self, serialized_job: JobModel) -> Job:
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
