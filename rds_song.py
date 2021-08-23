#!/usr/bin/python
import os
import sqlite3
import time
import tempfile

#tmpdir = tempfile.mkdtemp()
rdsctl = os.path.join('/tmp','rds_ctl')
dbpath="/srv/media/radio"
last_song=''
if not os.path.exists(rdsctl):
#    os.remove(rdsctl)
    os.mkfifo(rdsctl)
fifo=open(rdsctl,"w",1)
texto="RADIOVROCK FM   "
c=0
size=8
jump=2
sleep=4
#completa texto com marquee de final
length = len(texto)
texto=texto
for x in range(size):
	texto=texto+texto[x]

while(True):
	con=sqlite3.connect(os.path.join(dbpath,"radio.db"))
	cur=con.cursor()
	cur.execute("SELECT song_name from music_played order by date_played desc")
	song_name=cur.fetchone()[0]
	cur.close()
	marquee=''
	for x in range(size):
		marquee=marquee+texto[x+c]
		if x+c+1 >= len(texto):
			c=0
			break
	c=c+jump	
	if(last_song != song_name):
	    last_song=song_name
	    command = "RT "+song_name.encode("UTF-8")
	else:
	    command = "PS "+marquee
        try:
            fifo.write(command+"\n")
        except Exception:
            print("Unable to write to named pipe") 
	time.sleep(sleep)
