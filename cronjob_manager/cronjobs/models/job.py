from typing import Dict
from uuid import uuid4
from django.conf import settings
from django.db import models
from datetime import datetime
from enums import JobStatus
import pytz


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    u_id = models.UUIDField(default=uuid4)
    key = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    next_run_time = models.DateTimeField()
    job_state = models.BinaryField(null=True)
    status = models.CharField(max_length=20, default=JobStatus.SCHEDULED.value)
    result = models.TextField()

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'u_id': str(self.u_id),
            'key': self.key,
            'created_at': datetime.strftime(self.created_at.astimezone(pytz.timezone('UTC')),
                                            settings.DEFAULT_DATETIME_FORMAT),
            'next_run_time': datetime.strftime(self.next_run_time.astimezone(pytz.timezone('UTC')),
                                               settings.DEFAULT_DATETIME_FORMAT),
            'status': self.status,
            'result': self.result,
        }

    def _deserialize_job(self):
        pass
