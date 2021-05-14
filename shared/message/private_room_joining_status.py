from enum import Enum


class PrivateRoomJoiningStatus(Enum):
    SUCCESS = 1
    ROOM_FULL = 2
    ROOM_NOT_EXIST = 3
    KICKED_FROM_ROOM = 4
