#!/usr/bin/env bash
git checkout sub
git_sync () {
	git branch --set-upstream-to=origin/sub
	git add --all
        git remove youtube-dl
	git config --global user.email "not.real@fake-email.com"
	git config --global user.name "Wumbee"
	git commit -am 'remote sync'
	git config pull.rebase false
	git push
}

touch BOTCONDITION
izuku () {
	while [ -f BOTCONDITION ]
	  do
	  mkdir -p logs
	  git pull
	  python3 src/main.py
	  git_sync
	  done
}
pip install -r requirements.txt
izuku
