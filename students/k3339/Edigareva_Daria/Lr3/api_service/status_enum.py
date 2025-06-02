from enum import StrEnum


class StatusEnum(StrEnum):
    pending = "pending"
    processing = "processing"
    success = "success"
    failure = "failure"