#!/usr/bin/python
import os,  random, subprocess, sqlite3,requests, time, re
from datetime import datetime
from listfiles import listfiles

audioext = ('.mp3','.m4a')
downloadvozdobrasil = "https://redenacionalderadio.com.br/programas/a-voz-do-brasil-download"
path="/srv/media/radio/music"
dbpath="/var/opt/radio"
hw="dmix:CARD=Loopback,DEV=0"
overlap=3 #Overlap time between songs. Only available if not piping the output
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

# @media - Media file or url
# @songname - Name of song to register
# @waittime - Time to sleep before retorning function as done
def playffmpeg(media,songname):
    try:
        regsongname(songname)
    except Exception:
        print("Unable to update song name")
    cmdffmpeg = ["ffmpeg","-i",media,"-loglevel","error","-f","wav","-bitexact", "-acodec", "pcm_s16le", "-ar", "48000", "-ac", "2"];
    if filtercomplex is not None:
        cmdffmpeg.append("-filter_complex")
        cmdffmpeg.append(filtercomplex)
    print("["+datetime.today().strftime("%d/%m/%Y - %H:%M:%S"+"]")+" Song: "+songname.encode("UTF-8"))
    if usehw: #If alsahw was used, output to alsa
        cmdffmpeg.append("-f")
        cmdffmpeg.append("alsa")
        cmdffmpeg.append(hw)
        psffmpeg = subprocess.Popen(cmdffmpeg)
    else: #pipe ffmpeg to fifo
        if not os.path.exists(broadfifo):
            os.mkfifo(broadfifo)
        cmdffmpeg.append("=") #set the output to pipe
        try:
            broadcast = open(broadfifo,"w")
        except Exception:
            print("Unable to write to broadpipe")
        psffmpeg = subprocess.Popen(cmdffmpeg,stdout=broadcast)
    return psffmpeg
    
def getsonglength(media):
    c = ['ffprobe','-v','error','-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', media]
    proc = subprocess.Popen(c,stdout=subprocess.PIPE)
    return proc.stdout.read()

#Overlap only works using downmix hardware and not overlapping
def playoverlapping(media,songname):
    psffmpeg = playffmpeg(media,songname)
    if(usehw and overlap > 0):
        length = getsonglength(media)
        if (length is not None):
            time.sleep(float(length) - overlap) #sleep manually and freed the routine to start another song
        else:
            psffmpeg.wait()
    else:
        psffmpeg.wait()

def vozdobrasil():
        #verifica se eh dia de semana (0 a 4) e se sao 21h
    if datetime.today().weekday() in range(0,5) and datetime.now().strftime("%H")=="21": #Verifica se eh dia util e a hora
        print("Iniciando transmissao da Voz do brasil")
        today=datetime.today()
        strtoday=today.strftime("%d-%m-%y")
        try:
	    resp = requests.get(downloadvozdobrasil)
            lines = resp.content.split("\n")
            for line in lines:
                if re.search(strtoday,line):
                    vozlink=line.split("\"")[1]
                    print("link: "+vozlink)
                    if vozlink is not None:
                        ps = playffmpeg(vozlink,"A Voz do Brasil")
                        ps.wait()
        except Exception:
            print('Nao foi possivel transmitir a voz do brasil') 


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
            playoverlapping(file,songname)
