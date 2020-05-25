import time
import os
import datetime
import sqlite3
import re

# import tkinter as tk


def fetch_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    temp = str(temp)
    #temp = temp.replace("'C", '')
    #temp = temp.replace('temp=', '')
    #temp = temp.replace('temp=', '')
    temp = re.search(r'\d+', temp)
    temp = int(temp.group(0))
    return temp


def push2db(row):
    db = sqlite3.connect("temp.sqlite")
    c = db.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS temps
            (UTC_Time TEXT, Temp INTEGER)''')
    c.executemany('''INSERT INTO temps(UTC_Time, Temp)
                VALUES(?,?)''', row)
    db.commit()
    print(f"Added {row}")
    db.close()


while True:
    temp = fetch_temp()
    horodate = datetime.datetime.utcnow()
    row = [(horodate, temp)]
    push2db(row)
    time.sleep(30)
