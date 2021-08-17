import os
import subprocess
import tempfile

freq="91.5"

#tmpdir = tempfile.mkdtemp()
rds_ctl = os.path.join('/tmp','rds_ctl')

subprocess.Popen(["mkfifo",rds_ctl])
rec = subprocess.Popen(["arecord", "-fS16_LE", "-r", "44100", "-Dplughw:0,0", "-c", "2", "-"],stdout=subprocess.PIPE)
fm = subprocess.Popen(["pi_fm_adv","--ps", "", "-f" , freq, "--audio", "-", "--ctl", rds_ctl,"--pty","11","--rt",""], stdin=rec.stdout, stdout=subprocess.PIPE)
rec.stdout.close()
output = fm.communicate()[0]
print(output)
