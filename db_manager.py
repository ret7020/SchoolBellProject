import sqlite3
from werkzeug.security import check_password_hash

class Db:
    def __init__(self, path_to_db="./data/db"):
        self.path_to_db = path_to_db
        self.connection = sqlite3.connect(self.path_to_db, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def update_timemanager(self, tm):
        self.tm = tm

    def get_timetable(self):
        dt = self.cursor.execute("SELECT `timetable`.*, `melodies`.filename FROM `timetable`, `melodies` WHERE `timetable`.melody_id = `melodies`.id").fetchall()
        return dt

    def check_password(self, user_pass_hash):
        real_pass_hash = self.cursor.execute('SELECT `password` FROM `config`').fetchone()[0]
        return check_password_hash(real_pass_hash, user_pass_hash)
        

    def get_config(self):
        dt = self.cursor.execute('SELECT * FROM `config`').fetchone()
        res = {"password_hash": dt[0], "building_number": dt[1]}
        return res

    def update_timetable(self, timetable):
        self.cursor.execute('UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME="timetable";')
        self.cursor.execute('DELETE FROM `timetable`')
        for lesson in timetable:
            self.cursor.execute('INSERT INTO "main"."timetable"("time_start", "time_finish", "melody_id") VALUES (?, ?, ?)', (lesson[0], lesson[1], 1))
        self.connection.commit()
        self.tm.update_timetable()

    def get_lesson(self, lesson_id):
        dt = self.cursor.execute('SELECT * FROM `timetable` WHERE `id` = ?', (lesson_id, )).fetchone()
        return dt

    def update_lesson(self, lesson_id, lesson_start, lesson_finish, melody_id, saturday_work=False, sunday_work=False):
        self.cursor.execute('UPDATE `timetable` SET `time_start` = ?, `time_finish` = ?, `melody_id` = ?, `saturday_work` = ?, `sunday_work` = ? WHERE `id` = ?', (lesson_start, lesson_finish, melody_id, saturday_work == "1", sunday_work == "1", lesson_id))
        self.connection.commit()
        self.tm.update_timetable()

    def get_all_melodies(self, only_names=False):
        dt = self.cursor.execute('SELECT * FROM `melodies`').fetchall()
        if only_names:
            new_dt = []
            for melody in dt:
                melody = list(melody)
                melody[2] = melody[2].split("/")[-1]
                new_dt.append(melody)
            dt = new_dt.copy()
        return dt

    def add_melody(self, filename, display_name):
        filename = f"./data/sounds/{filename}"
        self.cursor.execute('INSERT INTO "melodies" ("display_name", "filename") VALUES (?, ?)', (display_name, filename))
        self.connection.commit()
        return self.cursor.lastrowid

    def update_melody_title(self, melody_id, melody_new_name):
        self.cursor.execute('UPDATE `melodies` SET `display_name` = ? WHERE `id` = ?', (melody_new_name, melody_id))
        self.connection.commit()

    def update_config(self, building_number, new_password):
        if building_number:
            self.cursor.execute('UPDATE `config` SET `school_building_num` = ?', (building_number, ))
        self.connection.commit()

if __name__ == "__main__":
    print("[DEBUG] Testing db manager library")
    dbm = Db()
    print(dbm.get_all_melodies())