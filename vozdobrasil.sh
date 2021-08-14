#!/bin/sh
omxplayer $(curl -L https://redenacionalderadio.com.br/programas/a-voz-do-brasil-download | grep date +%d-%m-%y | awk 'BEGIN { FS = "\"" } ; {print $2}')
