from db_manager import Db
from audio import AudioManager
from time_manager import TimeController
import threading
from cli import CLI
from web import WebUI, MelodiesStorage


if __name__ == "__main__":
    dbm = Db("./data/db")
    aud = AudioManager()
    tm = TimeController(dbm)
    dbm.update_timemanager(tm)
    melodies_storage = MelodiesStorage()
    web = WebUI(__name__, dbm, tm, melodies_storage, dev_mode=True)
    threading.Thread(target=lambda: tm.check_loop(aud)).start()
    threading.Thread(target=lambda: web.run()).start()
    cli = CLI()
    cli.controller(tm)
