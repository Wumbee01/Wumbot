#!/usr/bin/env bash

# installing dependencies
pip install discord.py
git clone https://github.com/hakureii/izuku.git

# setting up workdir
WORK=$(pwd)/izuku

function looper () {
	while true
		python3 $WORK/src/main.py $@
}

function slayer () {
	sleep $(( 4 * 60 * 60 ))
	kill $@
}

looper $@ &
slayer $!
