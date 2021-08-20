#!/usr/bin/python

import os
import stat
import subprocess
import tempfile
import time
from datetime import datetime

freq="91.5"
ps="VROCK FM"
rt="RADIOVROCK FM"
fm=None
sleeptime=7200
usehw=False
broadfifo=os.path.join("/tmp","broadcast")
#tmpdir = tempfile.mkdtemp()
rds_ctl = os.path.join('/tmp','rds_ctl')
subprocess.Popen(["mkfifo",rds_ctl])


def startfm():
    inputbroadcast = "-" #Imput for pi_fm_adv. If hardware is true, the input is piped from arecord
    arecord=["arecord", "-fS16_LE", "-r", "44100", "-Dplughw:0,0", "-c", "2", "-", "--quiet"]
    time.sleep(0.3)
    pifmadv=["pi_fm_adv","--wait","0","--ps", ps,"--freq" , freq, "--ctl", rds_ctl,"--rt",rt,"--mpx","40","--preemph","us","--audio"]
    if usehw:
        pifmadv.append("-")
        rec = subprocess.Popen(arecord,stdout=subprocess.PIPE)
        fm = subprocess.Popen(pifmadv, stdin=rec.stdout, stdout=subprocess.PIPE)
        rec.stdout.close()
    else:
        subprocess.Popen(["mkfifo",broadfifo])
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
