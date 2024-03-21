from enum import StrEnum


class Priority(StrEnum):
    trivial = "trivial"
    blocker = "blocker"
    critical = "critical"
    major = "major"
    minor = "minor"


class Status(StrEnum):
    open = "open"
    in_progress = "in_progress"
    done = "done"


class LinkStatus(StrEnum):
    is_blocked_by = "is_blocked_by"
    blocks = "blocks"
