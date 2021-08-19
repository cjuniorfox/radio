#!/usr/bin/python

import os
import subprocess
import tempfile
import time
from datetime import datetime

freq="91.5"
ps="VROCK FM"
rt="RADIOVROCK FM"
fm=None

#tmpdir = tempfile.mkdtemp()
rds_ctl = os.path.join('/tmp','rds_ctl')
subprocess.Popen(["mkfifo",rds_ctl])

#FM inside while loop to workaround this bug: https://github.com/miegl/PiFmAdv/issues/40
count=2 #Counter set to start exiter
hour=30 #Some hour it not exist

def startfm():
    time.sleep(0.3)
    rec = subprocess.Popen(["arecord", "-fS16_LE", "-r", "44100", "-Dplughw:0,0", "-c", "2", "-", "--quiet"],stdout=subprocess.PIPE)
    fm = subprocess.Popen(["pi_fm_adv","--wait","0","--ps", ps,"--freq" , freq, "--audio", "-", "--ctl", rds_ctl,"--rt",rt,"--mpx","40","--preemph","us"], stdin=rec.stdout, stdout=subprocess.PIPE)
    rec.stdout.close()
    return fm

def stopfm(fm):
    fm.terminate()
    fm.wait()
    return fm;

while(True):
    hournow = datetime.now().hour #obtain the hour to comare with
    if hournow != hour : 
        hour = hournow
        if count > 1 :
            count = 0
            print("Starting or Restarting the FM Exciter")
            if fm is not None :
                stopfm(fm)
            fm = startfm()
        else:
            count = count + 1
    time.sleep(60)
