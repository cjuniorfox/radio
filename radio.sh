#!/bin/sh
cd /srv/media/radio && python radio.py && echo $!>/tmp/radio.pid
