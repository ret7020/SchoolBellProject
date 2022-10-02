from db_manager import Db
from audio import AudioManager
from time_manager import TimeController
import threading
from cli import CLI
from web import WebUI, MelodiesStorage
from config import *

if __name__ == "__main__":
    dbm = Db(DB_PATH)
    aud = AudioManager()
    tm = TimeController(dbm)
    dbm.update_timemanager(tm)
    melodies_storage = MelodiesStorage(SOUNDS_DIR_PATH)
    web = WebUI(__name__, dbm, tm, aud, melodies_storage, FLASK_SECRET_KEY, host=WEB_HOST, port=WEB_PORT)
    threading.Thread(target=lambda: tm.check_loop(aud)).start()
    threading.Thread(target=lambda: web.run()).start()
    if START_CLI:
        cli = CLI(tm, dbm)
        cli.controller()
