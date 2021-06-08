import asyncio

import websockets

from server.connection_pool import ConnectionPool
from server.database import DBConnection
from server.game_room.game_room_service import GameRoomService
from server.message_broker import MessageBroker
from server.player.auth_service import AuthService
from server.player.player_repo import PlayerRepository
from shared import yaml_loader


CONFIG_FILE = "server-config.yaml"


if __name__ == "__main__":
    print("Server is running!")

    config = yaml_loader.load(CONFIG_FILE, {
        "websocket-port": 80,
        "db": {
            "username": "user",
            "password": "pass",
            "host": "localhost",
            "port": 27017,
            "database": "admin"
        }
    })

    db_conn = DBConnection(config["db"])
    player_repo = PlayerRepository(db_conn)
    auth_service = AuthService(player_repo)
    game_room_service = GameRoomService(player_repo)
    message_broker = MessageBroker(auth_service, game_room_service)
    connection_pool = ConnectionPool(message_broker)

    server = websockets.serve(connection_pool.handle_connection, port=config["websocket-port"])
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.gather(connection_pool.monitor_unauthenticated(), game_room_service.start_matching_players())
    asyncio.get_event_loop().run_forever()

    print("Server is closing")
