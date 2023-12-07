#!/usr/bin/env bash
git checkout sub
git_sync () {
        git checkout main
	git add --all
	git config --global user.email "not.real@fake-email.com"
	git config --global user.name "Wumbee"
	git commit -am 'sync main'
	git config pull.rebase false
	git push origin sub
}

touch BOTCONDITION
izuku () {
	while [ -f BOTCONDITION ]
	  do
	  mkdir -p logs
	  python3 src/main.py
	  git_sync
	  done
}
pip install -r requirements.txt
izuku
