#!/bin/bash

TOKEN=$1

ninstance=$(ps aux | grep telegramAlertsBotLauncher.sh | grep -v grep | wc -l)

if [[ $ninstance -le 2 ]] ; then
    while (true); do
		git pull -r origin main
		./fdaemon.py $TOKEN
        if [[ $? != 0 ]]; then
            exit 1
        fi
        sleep $(( $RANDOM % 30 + 1 ))
	done
else
	exit 0
fi

