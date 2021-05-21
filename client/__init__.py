import platform
import threading

from client.connection.connection_manager import ConnectionManager
from client.gui.gui_manager import GuiManager
from client.connection.auth_service import AuthService

if platform.system() == "Windows":
    # Workaround for getting wrong screen resolution in Windows
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except:
        ctypes.windll.user32.SetProcessDPIAware()


if __name__ == "__main__":
    print("Client is running!")

    connection_manager = ConnectionManager()
    auth_service = AuthService(connection_manager)
    gui = GuiManager(auth_service)
    connection_manager.set_notify_message(gui.notify_message)

    threading.Thread(target=connection_manager.start, daemon=True).start()

    gui.start()
