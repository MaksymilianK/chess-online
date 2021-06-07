from client.connection.auth_service import PlayerValidationStatus
from shared.message.auth_status import AuthStatus
from shared.message.private_room_joining_status import PrivateRoomJoiningStatus

VALIDATION_MESSAGES = {
    PlayerValidationStatus.INVALID_NICK: "Nick may consist of digits, letters ans underscores and should have length"
                                         "between 3 and 16 characters",
    PlayerValidationStatus.INVALID_EMAIL: "Wrong email format",
    PlayerValidationStatus.INVALID_PASSWORD: "Password should have length between 7 and 75 characters"
}

AUTH_MESSAGES = {
    AuthStatus.EMAIL_EXIST: "Email is already taken",
    AuthStatus.EMAIL_NOT_EXIST: "Email is not associated with any player",
    AuthStatus.NICK_EXIST: "Nick is already taken",
    AuthStatus.WRONG_PASSWORD: "Wrong password"
}

INVALID_ACCESS_KEY_MESSAGE = "Room access key should consist of 5 letters"
PRIVATE_ROOM_MESSAGES = {
    PrivateRoomJoiningStatus.ROOM_FULL.value: "Room is already full",
    PrivateRoomJoiningStatus.ROOM_NOT_EXIST.value: "Room with given access key does not exist",
    PrivateRoomJoiningStatus.KICKED_FROM_ROOM.value: "You were kicked from this room"
}
