#!/usr/bin/env bash

# installing dependencies
pip install py-cord
pip install urllib3
pip install args
pip install tasks
pip install option
pip install numpy
pip install python-dotenv
pip install openai
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
