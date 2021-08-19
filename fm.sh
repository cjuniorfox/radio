#!/bin/sh
cd /srv/media/radio && python fm.py && echo $!>/tmp/fm.pid
