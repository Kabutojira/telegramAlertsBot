#!/bin/bash

TOKEN=$1

ninstance=$(ps aux | grep telegramAlertsBotLauncher.sh | grep -v grep | wc -l)

#echo "$(date) $ninstance" >> z.log
#echo "$(date) $(ps aux | grep telegramAlertsBotLauncher.sh | grep -v grep) " >> z.log

if [[ $ninstance -le 5 ]] ; then
    while (true); do
        #echo "$(date) run" >> z.log
		git pull -r origin main
		./fdaemon.py $TOKEN
        sleep $(( $RANDOM % 30 + 1 ))
	done
else
    #echo "$(date) exit" >> z.log
	exit 0
fi

