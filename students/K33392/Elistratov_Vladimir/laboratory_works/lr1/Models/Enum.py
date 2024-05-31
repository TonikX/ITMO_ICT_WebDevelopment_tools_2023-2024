from enum import Enum


class States(Enum):
    awaiting = "awaiting"
    approve = "approve"
    reject = "reject"


class TransportType(Enum):
    plane = "plane"
    car = "car"
    truck = "truck"
    bus = "bus"
    other = "other"