import pytest

from server.game.game_runner import GameRunner
from server.game_room.game_room import PrivateGameRoom, RankedGameRoom
from server.game_room.game_room_service import GameRoomService
from shared.chess_engine.piece import Team
from shared.game.game_type import GameType
from shared.message.message_code import MessageCode
from shared.message.private_room_joining_status import PrivateRoomJoiningStatus
from tests.server.fakes import FakePlayerRepository, FakePlayer


@pytest.mark.asyncio
async def test_join_ranked_queue():
    service = GameRoomService(FakePlayerRepository())
    player1 = FakePlayer("player1", {GameType.BLITZ: 1000, GameType.RAPID: 1000, GameType.CLASSIC: 1000})
    player2 = FakePlayer("player2", {GameType.BLITZ: 1000, GameType.RAPID: 1000, GameType.CLASSIC: 999})
    player3 = FakePlayer("player3", {GameType.BLITZ: 4000, GameType.RAPID: 1000, GameType.CLASSIC: 1000})

    await service.join_ranked_queue(
        {"code": MessageCode.JOIN_RANKED_QUEUE.value, "gameType": GameType.RAPID.value},
        player1
    )
    await service.join_ranked_queue(
        {"code": MessageCode.JOIN_RANKED_QUEUE.value, "gameType": GameType.CLASSIC.value},
        player2
    )
    await service.join_ranked_queue(
        {"code": MessageCode.JOIN_RANKED_QUEUE.value, "gameType": GameType.BLITZ.value},
        player3
    )

    response = f'{{"code": {MessageCode.JOIN_RANKED_QUEUE.value}}}'

    assert player1 in service.ranked_queue[GameType.RAPID][10]
    assert player2 in service.ranked_queue[GameType.CLASSIC][9]
    assert player3 in service.ranked_queue[GameType.BLITZ][29]
    assert response in player1.sent_messages
    assert response in player2.sent_messages
    assert response in player3.sent_messages


@pytest.mark.asyncio
async def test_match_players():
    service = GameRoomService(FakePlayerRepository())
    player1 = FakePlayer("player1", {GameType.BLITZ: 1000, GameType.RAPID: 1200, GameType.CLASSIC: 1000})
    player2 = FakePlayer("player2", {GameType.BLITZ: 1000, GameType.RAPID: 4000, GameType.CLASSIC: 999})
    player3 = FakePlayer("player3", {GameType.BLITZ: 4000, GameType.RAPID: 4010, GameType.CLASSIC: 1000})
    player4 = FakePlayer("player4", {GameType.BLITZ: 1000, GameType.RAPID: 900, GameType.CLASSIC: 999})
    player5 = FakePlayer("player5", {GameType.BLITZ: 4000, GameType.RAPID: 1000, GameType.CLASSIC: 1000})

    service.ranked_queue[GameType.RAPID][12].add(player1)
    service.ranked_queue[GameType.RAPID][29].add(player2)
    service.ranked_queue[GameType.RAPID][29].add(player3)
    service.ranked_queue[GameType.RAPID][9].add(player4)
    service.ranked_queue[GameType.RAPID][9].add(player5)

    await service.match_players()

    assert len(service.ranked_queue[GameType.RAPID][12]) == 1
    assert len(service.ranked_queue[GameType.RAPID][29]) == 0
    assert len(service.ranked_queue[GameType.RAPID][9]) == 0
    assert len(service.ranked_queue[GameType.RAPID][10]) == 0

    assert len(service.ranked_rooms) == 2 * 2  # 2 room, 2 players each
    assert player1 not in service.ranked_rooms
    assert service.ranked_rooms[player2] is service.ranked_rooms[player3]
    assert service.ranked_rooms[player4] is service.ranked_rooms[player5]
    assert service.ranked_rooms[player2].runner.running
    assert service.ranked_rooms[player4].runner.running
    assert service.ranked_rooms[player2].runner.game_type == GameType.RAPID
    assert service.ranked_rooms[player2].runner.game_type == GameType.RAPID


@pytest.mark.asyncio
async def test_cancel_joining_ranked():
    service = GameRoomService(FakePlayerRepository())
    player1 = FakePlayer("player1", {GameType.BLITZ: 1000, GameType.RAPID: 1200, GameType.CLASSIC: 1000})
    player2 = FakePlayer("player2", {GameType.BLITZ: 1000, GameType.RAPID: 4000, GameType.CLASSIC: 999})
    player3 = FakePlayer("player3", {GameType.BLITZ: 4000, GameType.RAPID: 4010, GameType.CLASSIC: 1000})

    service.ranked_queue[GameType.RAPID][12].add(player1)
    service.ranked_queue[GameType.RAPID][29].add(player2)
    service.ranked_queue[GameType.RAPID][29].add(player3)

    await service.cancel_joining_ranked({}, player2)

    assert len(service.ranked_queue[GameType.RAPID][12]) == 1
    assert len(service.ranked_queue[GameType.RAPID][29]) == 1
    assert player2 not in service.ranked_queue[GameType.RAPID][29]

    message_str = f'{{"code": {MessageCode.CANCEL_JOINING_RANKED.value}}}'
    assert message_str in player2.sent_messages


@pytest.mark.asyncio
async def test_create_private_room():
    service = GameRoomService(FakePlayerRepository())
    player1 = FakePlayer("player1", {GameType.BLITZ: 1000, GameType.RAPID: 1200, GameType.CLASSIC: 1000})

    await service.create_private_room({}, player1)

    assert player1 in service.private_rooms_by_player
    room = service.private_rooms_by_player[player1]
    assert len(service.private_rooms_by_access_key) == 1
    assert room.host == player1
    assert len(room.access_key) == 5

    message_str = f'{{"code": {MessageCode.CREATE_PRIVATE_ROOM.value}, "accessKey": "{room.access_key}"}}'
    assert message_str in player1.sent_messages


@pytest.mark.asyncio
async def test_join_private_room():
    service = GameRoomService(FakePlayerRepository())
    player1 = FakePlayer("player1", {GameType.BLITZ: 1000, GameType.RAPID: 1200, GameType.CLASSIC: 1000})
    player2 = FakePlayer("player2", {GameType.BLITZ: 1000, GameType.RAPID: 4000, GameType.CLASSIC: 999})

    room = PrivateGameRoom(player1, GameRunner(), "ABCDE")

    service.private_rooms_by_player[player1] = room
    service.private_rooms_by_access_key["ABCDE"] = room

    await service.join_private_room(
        {"code": MessageCode.JOIN_PRIVATE_ROOM.value, "accessKey": "ABCDE"},
        player2
    )

    assert player2 in service.private_rooms_by_player
    assert room.guest is player2

    message = f'{{"code": {MessageCode.JOIN_PRIVATE_ROOM.value}, ' \
              f'"status": {PrivateRoomJoiningStatus.SUCCESS.value}, ' \
              f'"accessKey": "ABCDE", ' \
              f'"host": {{"nick": "player1", "elo": {{' \
              f'"{GameType.BLITZ.value}": 1000, "{GameType.RAPID.value}": 1200, "{GameType.CLASSIC.value}": 1000}}}}}}'

    assert message in player1.sent_messages
    assert message in player2.sent_messages


@pytest.mark.asyncio
async def test_leave_private_room():
    service = GameRoomService(FakePlayerRepository())
    player1 = FakePlayer("player1", {GameType.BLITZ: 1000, GameType.RAPID: 1200, GameType.CLASSIC: 1000})
    player2 = FakePlayer("player2", {GameType.BLITZ: 1000, GameType.RAPID: 4000, GameType.CLASSIC: 999})

    room = PrivateGameRoom(player1, GameRunner(), "ABCDE")
    room.guest = player2

    service.private_rooms_by_player[player1] = room
    service.private_rooms_by_player[player2] = room
    service.private_rooms_by_access_key["ABCDE"] = room

    await service.leave_private_room({}, player2)

    assert player1 in service.private_rooms_by_player
    assert player2 not in service.private_rooms_by_player
    assert "ABCDE" in service.private_rooms_by_access_key

    message = f'{{"code": {MessageCode.LEAVE_PRIVATE_ROOM.value}, "player": {{' \
              f'"nick": "player2", "elo": {{' \
              f'"{GameType.BLITZ.value}": 1000, "{GameType.RAPID.value}": 4000, "{GameType.CLASSIC.value}": 999}}}}}}'

    assert message in player1.sent_messages
    assert message in player2.sent_messages


@pytest.mark.asyncio
async def test_leave_private_room():
    service = GameRoomService(FakePlayerRepository())
    player1 = FakePlayer("player1", {GameType.BLITZ: 1000, GameType.RAPID: 1200, GameType.CLASSIC: 1000})
    player2 = FakePlayer("player2", {GameType.BLITZ: 1000, GameType.RAPID: 4000, GameType.CLASSIC: 999})

    room = PrivateGameRoom(player1, GameRunner(), "ABCDE")
    room.guest = player2

    service.private_rooms_by_player[player1] = room
    service.private_rooms_by_player[player2] = room
    service.private_rooms_by_access_key["ABCDE"] = room

    room.runner.start(player1, player2, GameType.BLITZ, lambda: None)

    await service.kick_from_private_room({}, player1)

    assert player1 in service.private_rooms_by_player
    assert player2 not in service.private_rooms_by_player
    assert "ABCDE" in service.private_rooms_by_access_key
    assert player2 in room.kicked
    assert not room.runner.running

    message = f'{{"code": {MessageCode.KICK_FROM_PRIVATE_ROOM.value}}}'
    assert message in player1.sent_messages
    assert message in player2.sent_messages


@pytest.mark.asyncio
async def test_start_private_game():
    service = GameRoomService(FakePlayerRepository())
    player1 = FakePlayer("player1", {GameType.BLITZ: 1000, GameType.RAPID: 1200, GameType.CLASSIC: 1000})
    player2 = FakePlayer("player2", {GameType.BLITZ: 1000, GameType.RAPID: 4000, GameType.CLASSIC: 999})

    room = PrivateGameRoom(player1, GameRunner(), "ABCDE")
    room.guest = player2

    service.private_rooms_by_player[player1] = room
    service.private_rooms_by_player[player2] = room
    service.private_rooms_by_access_key["ABCDE"] = room

    assert not room.runner.running

    await service.start_private_game(
        {"code": MessageCode.START_PRIVATE_GAME.value, "gameType": GameType.CLASSIC.value},
        player1
    )

    assert room.runner.running
    assert room.runner.game_type == GameType.CLASSIC


@pytest.mark.asyncio
async def test_surrender():
    player_repo = FakePlayerRepository()

    service = GameRoomService(player_repo)
    player1 = FakePlayer("player1", {GameType.BLITZ: 1000, GameType.RAPID: 1200, GameType.CLASSIC: 1000})
    player2 = FakePlayer("player2", {GameType.BLITZ: 1000, GameType.RAPID: 4000, GameType.CLASSIC: 999})

    room = RankedGameRoom(player1, player2, GameRunner())
    room.guest = player2

    service.ranked_rooms[player1] = room
    service.ranked_rooms[player2] = room

    room.runner.start(player1, player2, GameType.RAPID, lambda: None)

    await service.surrender({}, player1)

    assert not room.runner.running
    assert player1 not in service.ranked_rooms
    assert player2 not in service.ranked_rooms

    assert player_repo.players[0].elo[GameType.RAPID] < 1000
    assert player_repo.players[1].elo[GameType.RAPID] > 1240


@pytest.mark.asyncio
async def test_offer_draw():
    service = GameRoomService(FakePlayerRepository())
    player1 = FakePlayer("player1", {GameType.BLITZ: 1000, GameType.RAPID: 1200, GameType.CLASSIC: 1000})
    player2 = FakePlayer("player2", {GameType.BLITZ: 1000, GameType.RAPID: 4000, GameType.CLASSIC: 999})

    room = RankedGameRoom(player1, player2, GameRunner())
    room.guest = player2

    service.ranked_rooms[player1] = room
    service.ranked_rooms[player2] = room

    room.runner.start(player1, player2, GameType.RAPID, lambda: None)

    current_player = player1 if room.runner.teams[player1] == Team.WHITE else player2

    await service.offer_draw({}, current_player)

    assert player1 in service.ranked_rooms
    assert player2 in service.ranked_rooms

    assert len(player1.sent_messages) > 0
    assert len(player2.sent_messages) > 0

