import datetime
from db_manager import Db
from audio import AudioManager
import time

class TimeController:
    def __init__(self, dbm):
        self.dbm = dbm
        self.update_timetable()

    def update_timetable(self):
        self.timetable = self.dbm.get_timetable()

    def check_loop(self, aud):
        while True:
            for lesson in self.timetable:
                current_time_raw = datetime.datetime.now()
                current_time_fr = current_time_raw.strftime("%H:%M")
                if lesson[1] == current_time_fr or lesson[2] == current_time_fr:
                    #print("Bell!!!")
                    aud.ring_bell(lesson[4])
                    time.sleep(61 - datetime.datetime.now().second) # Sleep for one minute after bell rang

if __name__ == "__main__":
    dbm = Db("./data/db_dev")
    aud = AudioManager()
    tm = TimeController()
    tm.check_loop()
