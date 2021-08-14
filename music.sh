#!/bin/sh
while [ 1 -gt 0 ]; do   
	music=`ls /srv/media/radio/music/*.m4a | shuf -n 1`;
	if [ cat music.txt | grep 
done;
