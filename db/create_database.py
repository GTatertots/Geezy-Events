import os
import sqlite3

DB_FILE_NAME = "events.db"

TEST = False

def main():
    if os.path.exists(DB_FILE_NAME):
        os.remove(DB_FILE_NAME)



    con = sqlite3.connect(DB_FILE_NAME)
    cur = con.cursor()
    cur.execute("CREATE TABLE events (id INTEGER PRIMARY KEY, title TEXT, date TEXT, start_time TEXT, end_time TEXT, location TEXT, description TEXT, type TEXT)")
    if TEST:
        cur.execute("INSERT INTO events (title, date, start_time, end_time, location, description) VALUES ('test', 'test', 'test', 'test', 'test', 'test')")
        # cur.execute("SELECT title, date, start_time, end_time, location FROM events")
    con.commit()

if __name__ == "__main__":
    main()