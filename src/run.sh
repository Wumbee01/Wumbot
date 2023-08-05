#!/usr/bin/env bash

# installing dependencies
pip install pycord
git clone https://github.com/Wumbee01/Wumbot.git

# setting up workdir
WORK=$(pwd)/Wumbot

function looper () {
	while true
	do
		python3 $WORK/src/main.py $@
	done
}

function slayer () {
	sleep $(( 4 * 60 * 60 ))
	kill $@
}

looper $@ &
slayer $!
