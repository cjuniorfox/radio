import os
import random
import subprocess
import sqlite3

path='/srv/media/radio/music'
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

    print("Files and directories in a specified path")

    for filename in music_files:
        f=os.path.join(path,filename)
        if os.path.isfile(f):
            print(f)
            c = con.cursor()
            c.execute("SELECT plays from music_played where song_name = ?", (f,))
            if c.fetchone() is None:
                print("inserindo")
                c.execute("INSERT INTO music_played (song_name,plays,date_played) values (?,?,current_timestamp)",(f,1))
            else:
                c.execute("UPDATE music_played set (plays=plays+1,date_played=current_timestamp) where song_name=?"(f))
            con.commit()
            # subprocess.call(["omxplayer",f])
