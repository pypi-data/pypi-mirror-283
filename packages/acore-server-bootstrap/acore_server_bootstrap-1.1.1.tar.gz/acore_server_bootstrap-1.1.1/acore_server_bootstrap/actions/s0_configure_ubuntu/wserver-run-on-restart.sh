#!/bin/bash

sudo -H -u ubuntu /home/ubuntu/.pyenv/shims/python /home/ubuntu/git_repos/acore_server_bootstrap-project/acore_server_bootstrap/actions/s0_configure_ubuntu/wserver_run_on_restart.py
sudo /home/ubuntu/.pyenv/shims/python /home/ubuntu/git_repos/acore_server_bootstrap-project/acore_server_bootstrap/actions/s0_configure_ubuntu/wserver_run_on_restart_as_sudo.py
