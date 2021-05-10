import asyncio

import websockets

from server.connection_pool import ConnectionPool
from server.database import DBConnection, DBConfig
from server.message_broker import MessageBroker
from server.player.auth_service import AuthService
from server.player.player_repo import PlayerRepository

if __name__ == "__main__":
    print("Server is running!")

    config = DBConfig()
    db_conn = DBConnection(config)
    player_repo = PlayerRepository(db_conn)
    auth_service = AuthService(player_repo)
    message_broker = MessageBroker(auth_service)
    connection_pool = ConnectionPool(message_broker)

    server = websockets.serve(connection_pool.handle_connection, port=80)
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_until_complete(connection_pool.monitor_unauthenticated())
    asyncio.get_event_loop().run_forever()

    print("Server is closing")
