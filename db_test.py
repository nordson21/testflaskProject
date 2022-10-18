import sqlite3
from datetime import datetime


def add_message_in_db(user: str, message: str):
    with sqlite3.connect("site.db") as db:
        message_time = int(datetime.timestamp(datetime.now()))
        cur = db.cursor()
        cur.execute("""DROP TABLE IF EXISTS users""")
        cur.execute("""DROP TABLE IF EXISTS messages""")
        db.commit()


add_message_in_db('', 'Hello')
