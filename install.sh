#!/bin/bash
mkdir -p /opt/radio/lib /var/opt/radio
cp radio.py /opt/radio/
cp fm.py /opt/radio/
cp rds_song.py /opt/radio/
cp listfiles.py /opt/radio/lib
cp last_music.py /opt/radio/

ln -s /opt/radio/radio.py /usr/local/bin/radio
ln -s /opt/radio/fm.py /usr/local/bin/fm
ln -s /opt/radio/rds_song.py /usr/local/bin/rds_song
ln -s /opt/radio/last_music.py /usr/local/bin/last_music

cp radio.service /etc/systemd/system
cp rds_song.service /etc/systemd/system
cp fm.service /etc/systemd/system

systemctl enable radio rds_song fm
#systemctl start radio rds_song fm
