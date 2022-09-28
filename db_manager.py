import sqlite3

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

    def check_password(self):
        pass

    def get_config(self):
        dt = self.cursor.execute('SELECT * FROM `config`').fetchone()
        res = {"password_hash": dt[0], "building_number": dt[1]}
        return res

    def update_timetable(self, timetable):
        self.cursor.execute('UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME="timetable";')
        self.cursor.execute('DELETE FROM `timetable`')
        for lesson in timetable:
            self.cursor.execute('INSERT INTO "main"."timetable"("time_start", "time_finish", "melody_id") VALUES (?, ?, ?)', (lesson[0], lesson[1], 0))
        self.connection.commit()
        self.tm.update_timetable()

    def get_lesson(self, lesson_id):
        dt = self.cursor.execute('SELECT * FROM `timetable` WHERE `id` = ?', (lesson_id, )).fetchone()
        return dt

    def update_lesson(self, lesson_id, lesson_start, lesson_finish, melody_id):
        dt = self.cursor.execute('UPDATE `timetable` SET `time_start` = ?, `time_finish` = ?, `melody_id` = ? WHERE `id` = ?', (lesson_start, lesson_finish, melody_id, lesson_id))
        self.connection.commit()
        self.tm.update_timetable()

    def get_all_melodies(self):
        dt = self.cursor.execute('SELECT * FROM `melodies`').fetchall()
        return dt

    def add_melody(self, filename, display_name):
        dt = self.cursor.execute('INSERT INTO "melodies" ("display_name", "filename") VALUES (?, ?)', (display_name, filename))
        self.connection.commit()
        return self.cursor.lastrowid

    def update_melody_title(self, melody_id, melody_new_name):
        dt = self.cursor.execute('UPDATE `melodies` SET `display_name` = ? WHERE `id` = ?', (melody_new_name, melody_id))
        self.connection.commit()

if __name__ == "__main__":
    print("[DEBUG] Testing db manager library")
    dbm = Db()
    print(dbm.get_all_melodies())