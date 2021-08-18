import os
import sqlite3
import time
import tempfile

#tmpdir = tempfile.mkdtemp()
rds_ctl = os.path.join('/tmp','rds_ctl')
print(rds_ctl)
last_song=''

texto="RADIOVROCK FM"
c=0
size=8
jump=2
sleep=4
#completa texto com marquee de final
length = len(texto)
texto=texto+"   "
for x in range(size):
	texto=texto+texto[x]

while(True):
	con=sqlite3.connect("radio.db")
	cur=con.cursor()
	cur.execute("SELECT song_name from music_played order by date_played desc")
	song_name=cur.fetchone()[0]
	cur.close()
	marquee=''
	for x in range(size):
		marquee=marquee+texto[x+c].upper()
		if x+c+1 >= len(texto):
			c=0
			break
	c=c+jump	
	f=open(rds_ctl,"w")
	if(last_song != song_name):
		last_song=song_name
		print(song_name.encode("UTF-8"))
		f.write("RT "+song_name.upper())
	else:
		f.write("PS "+marquee)
	f.close()
	time.sleep(sleep)
