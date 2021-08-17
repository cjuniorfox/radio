import os
import time

texto="RADIOVROCK 91.5 FM"
c=0
size=8
#completa texto com marquee de final
length = len(texto)
texto=texto+"   "
for x in range(size):
	texto=texto+texto[x]

os.system('clear')
while(True):
	marquee=''
	for x in range(size):
		marquee=marquee+texto[x+c].upper()
		if x+c+1 >= len(texto):
			c=0
			break
	c=c+1
	print marquee + "          " + str(c)
	time.sleep(0.3)
	os.system('clear')

