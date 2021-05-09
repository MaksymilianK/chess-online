from enum import Enum


class PrivateRoomJoinStatus(Enum):
    ROOM_FULL = 1
    ROOM_NOT_EXIST = 2
    KICKED_FROM_ROOM = 3
