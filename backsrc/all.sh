#!/bin/bash -e
screen -d -m -RR django -t django bash -c 'cd /usr/local/lib/DialPro && source DialProvenv/bin/activate && cd /usr/local/lib/DialPro && git stash && git pull origin master && python manage.py runsslserver 0.0.0.0:8181'
#screen -d -m -RR node -t node bash -c 'cd /usr/local/lib/DialPro && node server.js'
#screen -d -m -RR worker -t worker bash -c 'cd /usr/local/lib && source DialProvenv/bin/activate && cd /usr/local/lib/DialPro && python manage.py shell'