import sqlite3

class Db:
    def __init__(self, path_to_db="./data/db"):
        self.path_to_db = path_to_db
        self.connection = sqlite3.connect(self.path_to_db, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_timetable(self):
        dt = self.cursor.execute("SELECT * FROM `timetable`").fetchall()
        return dt

    def get_melodies(self):
        pass

    def check_password(self):
        pass

    def get_config(self):
        dt = self.cursor.execute('SELECT * FROM `config`').fetchone()
        res = {"password_hash": dt[0], "building_number": dt[1]}
        return res

if __name__ == "__main__":
    print("[DEBUG] Testing db manager library")
    dbm = Db()
    print(dbm.get_config())