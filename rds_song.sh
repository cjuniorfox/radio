#!/bin/sh
cd /srv/media/radio && python rds_song.py && echo $!>/tmp/rds_song.pid
