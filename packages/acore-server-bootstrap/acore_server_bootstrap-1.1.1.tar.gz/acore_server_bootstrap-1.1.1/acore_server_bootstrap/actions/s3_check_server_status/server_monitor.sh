#!/bin/sh
# content of server_monitor.sh
# try to run measure server status cli command every 30 seconds
while :; do
~/git_repos/acore_soap_app-project/.venv/bin/acsoap canned measure-server-status
sleep 30
done
