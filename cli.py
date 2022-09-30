import datetime
from termcolor import colored
from audio import AudioManager

class CLI:
    def __init__(self, tm, dbm):
        self.tm = tm
        self.dbm = dbm
    def controller(self):
        while True:
            raw_cmd = input(">")
            if raw_cmd:
                splitted = raw_cmd.split()
                cmd = splitted[0]
                args = splitted[1:]
            else:
                continue
            if cmd == "tbs":
                print(f"Current time: {datetime.datetime.now()}")
                for lessons_counter in range(len(self.tm.timetable)):
                    lesson_finish = datetime.datetime.strptime(self.tm.timetable[lessons_counter][2], "%H:%M")
                    lesson_going_now = ""
                    if datetime.datetime.strptime(self.tm.timetable[lessons_counter][1], "%H:%M").time() <= datetime.datetime.now().time() < lesson_finish.time():
                        lesson_going_now = colored("NOW", "green")
                    print(f"Lesson #{lessons_counter + 1}: {self.tm.timetable[lessons_counter][1]}-{self.tm.timetable[lessons_counter][2]} {lesson_going_now}")
                    try:
                        next_lesson_start = datetime.datetime.strptime(self.tm.timetable[lessons_counter + 1][1], "%H:%M")
                        break_going_now = ""
                        if not lesson_going_now:
                            break_start = lesson_finish.time()
                            break_finish = next_lesson_start.time()
                            if break_start <= datetime.datetime.now().time() < break_finish:
                                break_going_now = colored("NOW", "green")
                        print(f"Break {int((next_lesson_start - lesson_finish).seconds / 60)} minutes {break_going_now}")
                    except IndexError:
                        pass
            elif cmd == "rtb":
                self.tm.update_timetable()
            elif cmd == "mbell":                
                tmp_aud = AudioManager()
                if len(args) > 0:
                    tmp_aud.ring_bell(args[0])
                else:
                    print("Add audio file name")

            elif cmd == "updl":
                new_start_time = args[0]
                new_finish_time = args[1]
                edit_lesson_id = args[2]
                melody_id = 1 # Default
                print(new_start_time, new_finish_time, edit_lesson_id)
                self.dbm.update_lesson(edit_lesson_id, new_start_time, new_finish_time, melody_id)
                self.tm.update_timetable() # Force update
