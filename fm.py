#!/usr/bin/python

import os
import stat
import subprocess
import tempfile
import time
from datetime import datetime

freq="91.5"
ps=""
rt=""
fm=None
sleeptime= 3600 * 2 #horas
usehw=True
broadfifo=os.path.join("/tmp","broadcast")
rdsctl = os.path.join("/tmp","rds_ctl")
mpx="70"
hwcard="hw:CARD=Loopback,DEV=1" # Obtain hw card with "aplay -L" command
equalizer="equalizer=f=440:width_type=o:width=2:g=5,equalizer=f=1000:width_type=h:width=200:g=-15,volume=1.5"

def startfm():
    inputbroadcast = "-" #Input for pi_fm_adv. If hardware is true, the input is piped from arecord
    comm_capture=["ffmpeg","-loglevel","error","-f","alsa","-i",hwcard,"-f","wav","-bitexact", "-acodec", "pcm_s16le", "-ar", "57000","-af",equalizer, "-ac", "2","-"]
    #arecord=["arecord", "-fS16_LE", "-r", "44100", "-Dplughw:0,0", "-c", "2", "-", "--quiet"]
    time.sleep(0.3)
    pifmadv=["pi_fm_adv","--wait","0","--ps", ps,"--freq" , freq,"--rt",rt,"--preemph","us","--mpx",mpx]
    #check if fifo exists
    if os.path.exists(rdsctl):
        pifmadv.append("--ctl")
        pifmadv.append(rdsctl)

    if usehw:
        pifmadv.append("--audio")
        pifmadv.append("-")
        rec = subprocess.Popen(comm_capture,stdout=subprocess.PIPE)
        fm = subprocess.Popen(pifmadv, stdin=rec.stdout, stdout=subprocess.PIPE)
        rec.stdout.close()
    else:
        pifmadv.append("--audio")
        pifmadv.append(broadfifo)
        fm = subprocess.Popen(pifmadv)
    return fm

def stopfm(fm):
    fm.terminate()
    fm.wait()
    return fm;

#FM inside while loop to workaround this bug: https://github.com/miegl/PiFmAdv/issues/40
while(True):
    print("Starting or Restarting the FM Exciter")
    if fm is not None :
        stopfm(fm)
    fm = startfm()
    time.sleep(sleeptime)
