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
        try:
            while True:
                for lesson in self.timetable:
                    current_time_raw = datetime.datetime.now()
                    current_time_fr = current_time_raw.strftime("%H:%M")
                    weekday = current_time_raw.weekday()
                    #weekday = 5 # for test
                    if lesson[1] == current_time_fr or lesson[2] == current_time_fr:
                        if (weekday == 5 and not lesson[4]) or (weekday == 6 and not lesson[5]): # Skip Sunday or Saturday bell
                            continue
                        aud.ring_bell(lesson[6])
                        time.sleep(61 - datetime.datetime.now().second) # Sleep for one minute after bell rang
        except Exception as e:
            print(e)
if __name__ == "__main__":
    dbm = Db("./data/db_dev")
    aud = AudioManager()
    tm = TimeController()
    tm.check_loop()
