# -*- coding: utf-8 -*-

"""
todo: docstring
"""

import fire
from acore_server.api import Server

from .. import api
from ..logger import logger


class Command:
    """
    acore server bootstrap command line interface.
    """

    def hello(self):
        """
        Print welcome message.
        """
        print("Hello acore server bootstrap user!")

    @logger.pretty_log()
    def bootstrap_as_sudo(self):
        """
        Bootstrap a new EC2 server, run automations that requires sudo.
        """
        with logger.nested():
            api.disable_ubuntu_auto_upgrade()
            api.setup_ec2_run_on_restart_script()

    @logger.pretty_log()
    def bootstrap(self):
        """
        Bootstrap a new EC2 server, run automations that doesn't require sudo.
        """
        with logger.nested():
            server = Server.from_ec2_inside()
            api.configure_db(server)
            api.apply_server_config(server)
            api.run_check_server_status_cron_job()
            api.run_server()

    def disable_ubuntu_auto_upgrade(self):
        """
        Disable Ubuntu auto upgrade (don't upgrade mysql).
        """
        api.disable_ubuntu_auto_upgrade()

    def setup_ec2_run_on_restart_script(self):
        """
        Setup cloud init script to run on restart.
        """
        api.setup_ec2_run_on_restart_script()

    def create_database(self):
        """
        Create the database user for game server and three initial databases.
        """
        server = Server.from_ec2_inside()
        api.create_database(server)

    def create_user(self):
        """
        Create the database user for game server.
        """
        server = Server.from_ec2_inside()
        api.create_user(server)

    def update_realmlist(self):
        """
        Update 'acore_auth.realmlist.address'.
        """
        server = Server.from_ec2_inside()
        api.update_realmlist(server)

    def configure_db(self):
        """
        Configure the database for game server.
        """
        server = Server.from_ec2_inside()
        api.configure_db(server)

    def apply_authserver_conf(self):
        """
        Update the authserver.conf.
        """
        server = Server.from_ec2_inside()
        api.apply_authserver_conf(server)

    def apply_worldserver_conf(self):
        """
        Update the worldserver.conf.
        """
        server = Server.from_ec2_inside()
        api.apply_worldserver_conf(server)

    def apply_mod_lua_engine_conf(self):
        """
        Update the mod_LuaEngine.conf.
        """
        server = Server.from_ec2_inside()
        api.apply_mod_lua_engine_conf(server)

    def apply_server_config(self):
        """
        Update the authserver.conf, worldserver.conf and mod_LuaEngine.conf.
        """
        server = Server.from_ec2_inside()
        api.apply_server_config(server)

    def sync_lua_scripts(self, s3dir_uri: str):
        api.sync_lua_scripts(s3dir_uri=s3dir_uri)

    def run_check_server_status_cron_job(self):
        """
        Run the "check server status" cron job in screen session.
        """
        api.run_check_server_status_cron_job()

    def stop_check_server_status_cron_job(self):
        """
        Stop the "check server status" cron job.
        """
        api.stop_check_server_status_cron_job()

    def run_server(self):
        """
        Run the game server in screen session.
        """
        api.run_server()

    def list_session(self):
        """
        List all screen sessions.
        """
        api.list_session()

    def enter_worldserver(self):
        """
        Enter the worldserver screen session.
        """
        api.enter_worldserver()

    def stop_server(self):
        """
        Stop the game server.
        """
        api.stop_server()


def run():
    fire.Fire(Command)
