from typing import Dict
from uuid import uuid4
from django.db import models
from datetime import datetime
import pytz


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    u_id = models.UUIDField(default=uuid4)
    key = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    next_run_time = models.DateTimeField()
    job_state = models.BinaryField()

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'u_id': str(self.u_id),
            'key': self.key,
            'created_at': datetime.strftime(self.created_at.astimezone(pytz.timezone('US/Pacific')),
                                            '%Y-%m-%d %H:%M:%S %Z%z'),
            'next_run_time': datetime.strftime(self.next_run_time.astimezone(pytz.timezone('US/Pacific')),
                                               '%Y-%m-%d %H:%M:%S %Z%z'),
            # 'job_state': self.job_state.hex(),
        }

    def _deserialize_job(self):
        pass
