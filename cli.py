import datetime

class CLI:
    def __init__(self):
        pass
    def controller(self, tm):
        while True:
            cmd = input(">")
            if cmd == "tbs":
                for lessons_counter in range(len(tm.timetable)):
                    print(f"Lesson #{lessons_counter + 1}: {tm.timetable[lessons_counter][1]}-{tm.timetable[lessons_counter][2]}")
                    try:
                        lesson_finish = datetime.datetime.strptime(tm.timetable[lessons_counter][2], "%H:%M")
                        next_lesson_start = datetime.datetime.strptime(tm.timetable[lessons_counter + 1][1], "%H:%M")
                        print(f"Break {int((next_lesson_start - lesson_finish).seconds / 60)} minutes")
                    except IndexError:
                        pass
                    