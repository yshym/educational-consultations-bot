from enum import Enum


class Category(Enum):
    BACKEND = "backend"
    FRONTEND = "frontend"

    @classmethod
    def values(cls):
        return list(map(lambda c: c.value, cls))
