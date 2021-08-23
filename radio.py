#!/usr/bin/python
import os
import stat
import random
import subprocess
import sqlite3
import requests
import re
from datetime import datetime
from listfiles import listfiles

audioext = ('.mp3','.m4a')
downloadvozdobrasil = "https://redenacionalderadio.com.br/programas/a-voz-do-brasil-download"
path="/srv/media/radio/music"
dbpath="/srv/media/radio"
audiohw="hw:0,0"
hw="dmix:CARD=Loopback,DEV=0"
#Define if the broadcast will use hardware (can be snd_aloop) or thought a fifo
usehw=True 
broadfifo=os.path.join('/tmp','broadcast') #Broadcast file (used only if usehw is false
filtercomplex="compand=attacks=0:points=-80/-900|-45/-15|-27/-9|0/-7|20/-7:gain=5" #filter options for ffmpeg conversion

def regsongname(song_name):
    c = con.cursor()
    c.execute("SELECT plays from music_played where song_name = ?", (song_name,))
    result=c.fetchone()
    if result is None:
        c.execute("INSERT INTO music_played (song_name,plays,date_played) values (?,?,current_timestamp)",(song_name,1))
    else:
        #Verifica se musica foi menos tocada que as demais da radio
        c.execute("UPDATE music_played set plays=plays+1,date_played=current_timestamp where song_name=?",(song_name,))
    con.commit()

def playffmpeg(media,songname):
    try:
        regsongname(songname)
    except E:
        print("Unable to update song name")
    cmdffmpeg = ["ffmpeg","-i",media,"-loglevel","error","-f","wav","-bitexact", "-acodec", "pcm_s16le", "-ar", "48000", "-ac", "2"];
    if filtercomplex is not None:
        cmdffmpeg.append("-filter_complex")
        cmdffmpeg.append(filtercomplex)
    print("["+datetime.today().strftime("%d/%m/%Y - %H:%M:%S"+"]")+" Song: "+songname.encode("UTF-8"))
    aplaycmd = ["aplay","-D",audiohw,"--quiet"]
    if usehw: #If alsahw was used, output to alsa
        cmdffmpeg.append("-f")
        cmdffmpeg.append("alsa")
        cmdffmpeg.append(hw)
        psffmpeg = subprocess.Popen(cmdffmpeg)
        #psaplay = subprocess.Popen(aplaycmd,stdin=psffmpeg.stdout,stdout=subprocess.PIPE)
        psffmpeg.wait()
        #print(psaplay.communicate()[0])
    else: #pipe ffmpeg to fifo
        if not os.path.exists(broadfifo):
            os.mkfifo(broadfifo)
        cmdffmpeg.append("=") #set the output to pipe
        try:
            broadcast = open(broadfifo,"w")
        except Exception:
            print("Unable to write to broadpipe")
        psffmpeg = subprocess.Popen(cmdffmpeg,stdout=broadcast)
        psffmpeg.wait()
    #psffmpeg.stdout.close()
    #print(psaplay.communicate()[0])
    
def vozdobrasil():
    if datetime.today().weekday() in range(0,4) and datetime.now().strftime("%H")=="21": #Verifica se eh dia util e a hora
        print("Voz do brasil")
        today=datetime.today()
        strtoday=today.strftime("%d-%m-%y")
        try:
	    resp = requests.get(downloadvozdobrasil)
            lines = resp.content.split("\n")
            for line in lines:
                if re.search(strtoday,line):
                    vozlink=line.split("\"")[1]
                    print(vozlink)
                    if vozlink is not None:
                        playffmpeg(vozlink,"A Voz do Brasil")
        except Exception:
            print('Unable to reach the internet') 


con= sqlite3.connect(os.path.join(dbpath,"radio.db"))
c = con.cursor();
#Check for creation of database
c.execute(" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='music_played' ")
if c.fetchone()[0]==0 :
	c.execute("CREATE TABLE music_played ([generated_id] INTEGER PRIMARY KEY,[song_name] text, [plays] integer default 0, [date_played] datetime default current_timestamp)")
con.commit()

while ( True ): #infinite loop
    musicfiles=listfiles(path,audioext)
    random.shuffle(musicfiles)

    for file in musicfiles:
        vozdobrasil()
        songname = file.rsplit('/',1)[1].decode('utf-8').replace('.m4a','').replace('.mp3','')
        if os.path.isfile(file):
            playffmpeg(file,songname)
