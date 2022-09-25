from db_manager import Db
from audio import AudioManager
from time_manager import TimeController
import threading
from cli import CLI
from web import WebUI


if __name__ == "__main__":
    dbm = Db("./data/db_dev")
    aud = AudioManager()
    tm = TimeController(dbm)
    web = WebUI(__name__)
    threading.Thread(target=lambda: tm.check_loop(aud)).start()
    threading.Thread(target=lambda: web.run()).start()
    cli = CLI()
    cli.controller(tm)
