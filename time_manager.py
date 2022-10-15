import datetime
from db_manager import Db
from audio import AudioManager
import time


class TimeController:
    '''
    Class to minotor time and send a bell ring request
    '''

    def __init__(self, dbm):
        self.dbm = dbm
        self.update_timetable()

    def update_timetable(self):
        self.timetable = self.dbm.get_timetable()
        self.mute_mode = self.dbm.get_mute_mode()

    def check_loop(self, aud):
        try:
            while True:                
                for lesson in self.timetable:
                    current_time_raw = datetime.datetime.now()
                    current_time_fr = current_time_raw.strftime("%H:%M")
                    weekday = current_time_raw.weekday()
                    # weekday = 5 # for test

                    # If it is time for bell
                    if lesson[1] == current_time_fr or lesson[2] == current_time_fr:
                        # Skip Sunday or Saturday bell
                        if (weekday == 5 and not lesson[4]) or (weekday == 6 and not lesson[5]):
                            continue  # Skip
                        bell_status = True
                        if self.mute_mode[0] == 1:
                            next_day_from_mute = self.mute_mode[1] + \
                                datetime.timedelta(days=1)
                            # If one from mute mode turned on finished we enable bell
                            if current_time_raw.date() >= next_day_from_mute.date():
                                self.mute_mode = [0, 0]
                                self.dbm.reset_mute_mode()
                            else:
                                bell_status = False  # disable
                        if bell_status:
                            aud.ring_bell(lesson[6])

                        # Sleep for one minute after bell rang. Protect from multiple bells per one minute
                        time.sleep(61 - datetime.datetime.now().second)
        except Exception as e:
            '''
            Skip temporary exceptions
            '''
            print(e)  # Dbg


if __name__ == "__main__":
    # Test
    # Deprecated
    dbm = Db("./data/db_dev")
    aud = AudioManager()
    tm = TimeController()
    tm.check_loop()
