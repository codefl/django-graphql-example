from enum import Enum


class Currency(Enum):
    USD = "USD"
    CAD = "CAD"
    EUR = "EUR"

    @classmethod
    def choices(cls):
        return [(i, i.value) for i in cls]
