# -*- coding: utf-8 -*-

import pytest
import sys
import subprocess
from pathlib import Path
from acore_server_bootstrap import api


def test():
    _ = api

    _ = api.disable_ubuntu_auto_upgrade
    _ = api.setup_ec2_run_on_restart_script
    _ = api.create_database
    _ = api.create_user
    _ = api.update_realmlist
    _ = api.configure_db
    _ = api.apply_authserver_conf
    _ = api.apply_worldserver_conf
    _ = api.apply_mod_lua_engine_conf
    _ = api.apply_server_config
    _ = api.sync_lua_scripts
    _ = api.run_check_server_status_cron_job
    _ = api.stop_check_server_status_cron_job
    _ = api.run_server
    _ = api.list_session
    _ = api.enter_worldserver
    _ = api.stop_server
    _ = api.Remoter


@pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")
def test_cli():
    path_cli = Path(sys.executable).parent.joinpath("acorebs")

    def _test_command(action: str):
        args = [f"{path_cli}", action, "-h"]
        subprocess.run(args, capture_output=True, check=True)

    actions = [
        "hello",
        "bootstrap_as_sudo",
        "bootstrap",
        "disable_ubuntu_auto_upgrade",
        "setup_ec2_run_on_restart_script",
        "create_database",
        "create_user",
        "update_realmlist",
        "configure_db",
        "apply_authserver_conf",
        "apply_worldserver_conf",
        "apply_mod_lua_engine_conf",
        "apply_server_config",
        "run_check_server_status_cron_job",
        "stop_check_server_status_cron_job",
        "run_server",
        "list_session",
        "enter_worldserver",
        "stop_server",
    ]
    for action in actions:
        _test_command(action)


if __name__ == "__main__":
    from acore_server_bootstrap.tests import run_cov_test

    run_cov_test(__file__, "acore_server_bootstrap.api", preview=False)
