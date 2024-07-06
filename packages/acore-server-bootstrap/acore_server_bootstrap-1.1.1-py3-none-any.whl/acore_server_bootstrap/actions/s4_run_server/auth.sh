#!/bin/sh
# content of auth.sh
# try to run authserver every 30 seconds, if already run, do nothing
# make sure your azerothcore server executable is at ${HOME}/azeroth-server/bin/

while :; do
~/azeroth-server/bin/authserver
sleep 30
done
