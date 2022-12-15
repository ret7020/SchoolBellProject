# THIS IS AN DB UPDATE SCRIPT
# From version 1.2.0 in db added column melody_finish_id and melody_id renamed to melody_start_id in table timetable
# This script will fix tables automatically
# STOP main.py TO prevent problems with connections to database

import sqlite3

DB_PATH = "../data/db" # PATH TO DATABASE FILE


if __name__ == "__main__":
    connection = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cursor = connection.cursor()

    try:
        connection.execute("ALTER TABLE timetable RENAME COLUMN melody_id TO melody_start_id")
        connection.commit()
    except sqlite3.OperationalError:
        pass

    try:
        connection.execute("ALTER TABLE `timetable` ADD COLUMN melody_finish_id integer default 1")
        connection.commit()
    except sqlite3.OperationalError:
        pass
    print("Updated")
