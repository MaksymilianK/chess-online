import platform
import threading

from client.connection.connection_manager import ConnectionManager
from client.connection.game_room_service import GameRoomService
from client.gui.gui_manager import GuiManager
from client.connection.auth_service import AuthService
from shared import yaml_loader

if platform.system() == "Windows":
    # Workaround for getting wrong screen resolution in Windows
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except:
        ctypes.windll.user32.SetProcessDPIAware()


CONFIG_FILE = "client-config.yaml"


if __name__ == "__main__":
    print("Client is running!")

    config = yaml_loader.load(CONFIG_FILE, {
        "host": "localhost",
        "port": 80
    })

    connection_manager = ConnectionManager(config)
    auth_service = AuthService(connection_manager)
    game_room_service = GameRoomService(connection_manager, auth_service)

    gui = GuiManager(auth_service, game_room_service)
    connection_manager.set_notify_message(gui.notify_message)

    threading.Thread(target=connection_manager.start, daemon=True).start()

    gui.start()
