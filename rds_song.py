#!/usr/bin/python
import os
import sqlite3
import time
import tempfile

#tmpdir = tempfile.mkdtemp()
rdsctl = os.path.join('/tmp','rds_ctl')
dbpath="/var/opt/radio"
last_song=''
if not os.path.exists(rdsctl):
#    os.remove(rdsctl)
    os.mkfifo(rdsctl)
fifo=open(rdsctl,"w",1)
texto="HEADBANGERS BALL"
marqueeEnabled=True
c=0
size=8
jump=8
sleep=10
#completa texto com marquee de final
length = len(texto)
texto=texto
if marqueeEnabled:
    for x in range(size):
        texto=texto+texto[x]

def rdsfifo(command):
    try:
        print(command)
        fifo.write(command+"\n")
    except Exception:
        print("Unable to write to named pipe")

while(True):
    con=sqlite3.connect(os.path.join(dbpath,"radio.db"))
    cur=con.cursor()
    cur.execute("SELECT song_name from music_played order by date_played desc")
    data=cur.fetchone()[0]
    artist_music = data.split('-')
    song_name=artist_music[0]+'-'+artist_music[1]
    cur.close()
    marquee=''
    if marqueeEnabled:
        for x in range(size):
	    marquee=marquee+texto[x+c]
            if x+c+1 >= len(texto):
	        c=0
	        break
    c=c+jump	
    if(last_song != song_name):
        last_song=song_name
        command = "RT "+song_name.encode("UTF-8")
        rdsfifo(command)
    if marqueeEnabled:
        command = "PS "+marquee
        rdsfifo(command)
    time.sleep(sleep)
