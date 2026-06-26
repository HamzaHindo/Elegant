from dataclasses import dataclass, field


@dataclass
class Employee:
    name: str
    daily_rate: int
    working_hours: int
    id: int = field(init=False)

    _id_counter = 1  # class variable

    def __post_init__(self):
        self.id = Employee._id_counter
        Employee._id_counter += 1


@dataclass
class Stylist:
    name: str
    daily_rate: int
    working_hours: int
    daily_target: int
    id: int = field(init=False)

    _id_counter = 1  # class variable

    def __post_init__(self):
        self.id = Employee._id_counter
        Employee._id_counter += 1
