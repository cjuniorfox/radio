import os
import subprocess
import tempfile
import time

freq="91.5"
ps="VROCK FM"
rt="RADIOVROCK FM"

sleephours=2

#tmpdir = tempfile.mkdtemp()
rds_ctl = os.path.join('/tmp','rds_ctl')
subprocess.Popen(["mkfifo",rds_ctl])

#FM inside while loop to workaround this bug: https://github.com/miegl/PiFmAdv/issues/40
while(True):
    rec = subprocess.Popen(["arecord", "-fS16_LE", "-r", "44100", "-Dplughw:0,0", "-c", "2", "-", "--quiet"],stdout=subprocess.PIPE)
    fm = subprocess.Popen(["pi_fm_adv","--wait","0","--ps", ps,"--freq" , freq, "--audio", "-", "--ctl", rds_ctl,"--rt",rt,"--mpx","40","--preemph","us", "--cutoff","150000"], stdin=rec.stdout, stdout=subprocess.PIPE)
    #print(fm.communicate()[0])
    rec.stdout.close()
    time.sleep(60*60*sleephours)
    rec.terminate()
    fm.terminate()
    rec.wait()
    fm.wait()
