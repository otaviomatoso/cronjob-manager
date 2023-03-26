from datetime import datetime
from django.conf import settings
from django.db import models
from typing import Dict


class File(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'location': self.location,
            'name': self.name,
            'created_at': datetime.strftime(self.created_at, settings.DEFAULT_DATETIME_FORMAT),
        }
