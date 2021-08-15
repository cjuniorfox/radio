import os
import random
import subprocess
import sqlite3
import requests
import re
from datetime import datetime
from datetime import timedelta

downloadvozdobrasil = "https://redenacionalderadio.com.br/programas/a-voz-do-brasil-download"
path='/srv/media/radio/music'

def vozdobrasil():
    if datetime.today().weekday() in range(0,4) and datetime.now().strftime("%H")=="21": #Verifica se eh dia util e a hora
        print("Voz do brasil")
        today=datetime.today() - timedelta(1)
        strtoday=today.strftime("%d-%m-%y")
        resp = requests.get(downloadvozdobrasil)
        lines = resp.content.split("\n")
        for line in lines:
            if re.search(strtoday,line):
                vozlink=line.split("\"")[1]
                print(vozlink)
                if vozlink is not None:
                    subprocess.call(["omxplayer",vozlink])

con= sqlite3.connect("radio.db")
c = con.cursor();
#Check for creation of database
c.execute(" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='music_played' ")
if c.fetchone()[0]==0 :
	c.execute("CREATE TABLE music_played ([generated_id] INTEGER PRIMARY KEY,[song_name] text, [plays] integer default 0, [date_played] datetime default current_timestamp)")
con.commit()

while ( 0 < 1 ): #infinite loop
    music_files=[]

    for file_name in os.listdir(path):
        music_files.append(file_name)
    random.shuffle(music_files)

    for song in music_files:
        vozdobrasil()
        f=os.path.join(path,song)
        if os.path.isfile(f):
            print(song)
            c = con.cursor()
            c.execute("SELECT plays from music_played where song_name = ?", (song.decode('utf-8'),))
            result=c.fetchone()
            if result is None:
                c.execute("INSERT INTO music_played (song_name,plays,date_played) values (?,?,current_timestamp)",(song.decode('utf-8'),1))
            else:
                #Verifica se musica foi menos tocada que as demais da radio
                c.execute("UPDATE music_played set plays=plays+1,date_played=current_timestamp where song_name=?",(song.decode('utf-8'),))
            con.commit()
        #subprocess.call(["omxplayer","-o","alsa",f])
