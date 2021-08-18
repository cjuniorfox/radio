#!/usr/bin/python
import os
import sqlite3

con=sqlite3.connect("radio.db")
cur=con.cursor()
cur.execute("SELECT * from music_played order by date_played desc limit 1")
print("result of query")
for result in cur.fetchall():
    print(result)
