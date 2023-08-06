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
main='https://raw.githubusercontent.com/Wumbee01/Wumbot/main/src/main.py'

function looper () {
	while true
	do
		python3 <(curl $main) $@
	done
}

function slayer () {
	sleep $(( 1 * 60 * 60 ))
	kill $@
}

looper $@
