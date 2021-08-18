#!/bin/sh
cd /srv/media/radio && python fm.py && echo $!>/tmp/fm.pid
#while :; do
#        cd /srv/media/radio && python fm.py &
#        pid=$!
#	echo $1>/tmp/fm.pid
#        sleep 10s
#        kill  $pid
#	sleep 2s
#done
