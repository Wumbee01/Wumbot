#!/usr/bin/env bash
git checkout sub
git_sync () {
        git checkout main
	git remote set-url origin https://${TOKEN}@github.com/Wumbee01/Wumbot.git
	git add --all
	git config --global user.email "not.real@fake-email.com"
	git config --global user.name "Wumbee"
	git commit -am 'sync main'
	git config pull.rebase false
        git pull origin main
        git push origin main:sub --force
}

fetch_updates () {
        git checkout main
	git pull
}

touch BOTCONDITION
izuku () {
	while [ -f BOTCONDITION ]
	  do
	  mkdir -p logs
	  python3 src/main.py
	  git_sync
          fetch_updates
	  done
}
pip install -r requirements.txt
izuku
