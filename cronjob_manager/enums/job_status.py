from enum import Enum


class JobStatus(Enum):
    SCHEDULED = 'SCHEDULED'
    RUNNING = 'RUNNING'
    DONE = 'DONE'
