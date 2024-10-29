from enum import Enum


class UserLevel(str, Enum):
    admin = "admin"
    user = "user"
    guest = "guest"
