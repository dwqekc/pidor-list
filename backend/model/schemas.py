from enum import Enum

class TypeAuth(Enum):
    google = "google"
    telegram = "telegram"

class InfoAccount(Enum):
    delay = 120

class InfoPUBSUB(Enum):
    type = "message"
