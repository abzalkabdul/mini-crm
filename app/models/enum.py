from enum import Enum

class Status(str, Enum):
    in_progres = "IN PROGRESS"
    expired = "EXPIRED"
    finished = "FINISHED"
    not_started = "NOT STARTED"
