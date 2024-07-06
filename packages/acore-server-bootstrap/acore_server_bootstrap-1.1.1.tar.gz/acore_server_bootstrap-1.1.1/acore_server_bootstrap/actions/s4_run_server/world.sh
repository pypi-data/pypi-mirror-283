#!/bin/sh
# content of world.sh
# try to run worldserver every 30 seconds, if already run, do nothing
# make sure your azerothcore server executable is at ${HOME}/azeroth-server/bin/

while :; do
~/azeroth-server/bin/worldserver
sleep 30
done
