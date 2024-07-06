# -*- coding: utf-8 -*-

import typing as T
import dataclasses

import aws_ssm_run_command.api as aws_ssm_run_command
from acore_server.api import Server
from acore_paths.api import path_acore_server_bootstrap_cli


if T.TYPE_CHECKING:  # pragma: no cover
    from mypy_boto3_ssm.client import SSMClient

run_shell_script_sync = aws_ssm_run_command.better_boto.run_shell_script_sync


@dataclasses.dataclass
class Remoter:
    ssm_client: T.Optional["SSMClient"] = dataclasses.field(default=None)
    server: T.Optional["Server"] = dataclasses.field(default=None)

    def _run(
        self,
        action: str,
        sudo: bool = False,
        ssm_client: T.Optional["SSMClient"] = None,
        server: T.Optional[Server] = None,
    ):
        command = f"{path_acore_server_bootstrap_cli} {action}"
        if sudo is False:
            command = f"sudo -H -u ubuntu {command}"
        if ssm_client is None:
            ssm_client = self.ssm_client
        if server is None:
            server = self.server
        command_invocation_list = run_shell_script_sync(
            ssm_client=ssm_client,
            commands=command,
            instance_ids=server.metadata.ec2_inst.id,
            delays=1,
        )
        command_invocation = command_invocation_list[0]
        print(command_invocation.StandardOutputContent.strip())
        return command_invocation

    def hello(
        self,
        ssm_client: T.Optional["SSMClient"] = None,
        server: T.Optional[Server] = None,
    ):
        """
        Run :meth:`acore_server_bootstrap.cli.main.Command.hello` remotely.
        """
        return self._run(
            action="hello",
            ssm_client=ssm_client,
            server=server,
        )

    def bootstrap_as_sudo(
        self,
        ssm_client: T.Optional["SSMClient"] = None,
        server: T.Optional[Server] = None,
    ):
        """
        Run :meth:`acore_server_bootstrap.cli.main.Command.bootstrap_as_sudo` remotely.
        """
        return self._run(
            action="bootstrap_as_sudo",
            ssm_client=ssm_client,
            server=server,
            sudo=True,
        )

    def bootstrap(
        self,
        ssm_client: T.Optional["SSMClient"] = None,
        server: T.Optional[Server] = None,
    ):
        """
        Run :meth:`acore_server_bootstrap.cli.main.Command.bootstrap` remotely.
        """
        return self._run(
            action="bootstrap",
            ssm_client=ssm_client,
            server=server,
        )

    def disable_ubuntu_auto_upgrade(
        self,
        ssm_client: T.Optional["SSMClient"] = None,
        server: T.Optional[Server] = None,
    ):
        """
        Run :meth:`acore_server_bootstrap.cli.main.Command.disable_ubuntu_auto_upgrade` remotely.
        """
        return self._run(
            action="disable_ubuntu_auto_upgrade",
            ssm_client=ssm_client,
            server=server,
            sudo=True,
        )

    def setup_ec2_run_on_restart_script(
        self,
        ssm_client: T.Optional["SSMClient"] = None,
        server: T.Optional[Server] = None,
    ):
        """
        Run :meth:`acore_server_bootstrap.cli.main.Command.setup_ec2_run_on_restart_script` remotely.
        """
        return self._run(
            action="setup_ec2_run_on_restart_script",
            ssm_client=ssm_client,
            server=server,
            sudo=True,
        )

    def create_database(
        self,
        ssm_client: T.Optional["SSMClient"] = None,
        server: T.Optional[Server] = None,
    ):
        """
        Run :meth:`acore_server_bootstrap.cli.main.Command.create_database` remotely.
        """
        return self._run(
            action="create_database",
            ssm_client=ssm_client,
            server=server,
        )

    def create_user(
        self,
        ssm_client: T.Optional["SSMClient"] = None,
        server: T.Optional[Server] = None,
    ):
        """
        Run :meth:`acore_server_bootstrap.cli.main.Command.create_user` remotely.
        """
        return self._run(
            action="create_user",
            ssm_client=ssm_client,
            server=server,
        )

    def update_realmlist(
        self,
        ssm_client: T.Optional["SSMClient"] = None,
        server: T.Optional[Server] = None,
    ):
        """
        Run :meth:`acore_server_bootstrap.cli.main.Command.update_realmlist` remotely.
        """
        return self._run(
            action="update_realmlist",
            ssm_client=ssm_client,
            server=server,
        )

    def configure_db(
        self,
        ssm_client: T.Optional["SSMClient"] = None,
        server: T.Optional[Server] = None,
    ):
        """
        Run :meth:`acore_server_bootstrap.cli.main.Command.configure_db` remotely.
        """
        return self._run(
            action="configure_db",
            ssm_client=ssm_client,
            server=server,
        )

    def apply_authserver_conf(
        self,
        ssm_client: T.Optional["SSMClient"] = None,
        server: T.Optional[Server] = None,
    ):
        """
        Run :meth:`acore_server_bootstrap.cli.main.Command.apply_authserver_conf` remotely.
        """
        return self._run(
            action="apply_authserver_conf",
            ssm_client=ssm_client,
            server=server,
        )

    def apply_worldserver_conf(
        self,
        ssm_client: T.Optional["SSMClient"] = None,
        server: T.Optional[Server] = None,
    ):
        """
        Run :meth:`acore_server_bootstrap.cli.main.Command.apply_worldserver_conf` remotely.
        """
        return self._run(
            action="apply_worldserver_conf",
            ssm_client=ssm_client,
            server=server,
        )

    def apply_mod_lua_engine_conf(
        self,
        ssm_client: T.Optional["SSMClient"] = None,
        server: T.Optional[Server] = None,
    ):
        """
        Run :meth:`acore_server_bootstrap.cli.main.Command.apply_mod_lua_engine_conf` remotely.
        """
        return self._run(
            action="apply_mod_lua_engine_conf",
            ssm_client=ssm_client,
            server=server,
        )

    def apply_server_config(
        self,
        ssm_client: T.Optional["SSMClient"] = None,
        server: T.Optional[Server] = None,
    ):
        """
        Run :meth:`acore_server_bootstrap.cli.main.Command.apply_server_config` remotely.
        """
        return self._run(
            action="apply_server_config",
            ssm_client=ssm_client,
            server=server,
        )

    def run_check_server_status_cron_job(
        self,
        ssm_client: T.Optional["SSMClient"] = None,
        server: T.Optional[Server] = None,
    ):
        """
        Run :meth:`acore_server_bootstrap.cli.main.Command.run_check_server_status_cron_job` remotely.
        """
        return self._run(
            action="run_check_server_status_cron_job",
            ssm_client=ssm_client,
            server=server,
        )

    def stop_check_server_status_cron_job(
        self,
        ssm_client: T.Optional["SSMClient"] = None,
        server: T.Optional[Server] = None,
    ):
        """
        Run :meth:`acore_server_bootstrap.cli.main.Command.stop_check_server_status_cron_job` remotely.
        """
        return self._run(
            action="stop_check_server_status_cron_job",
            ssm_client=ssm_client,
            server=server,
        )

    def run_server(
        self,
        ssm_client: T.Optional["SSMClient"] = None,
        server: T.Optional[Server] = None,
    ):
        """
        Run :meth:`acore_server_bootstrap.cli.main.Command.run_server` remotely.
        """
        return self._run(
            action="run_server",
            ssm_client=ssm_client,
            server=server,
        )

    def list_session(
        self,
        ssm_client: T.Optional["SSMClient"] = None,
        server: T.Optional[Server] = None,
    ):
        """
        Run :meth:`acore_server_bootstrap.cli.main.Command.list_session` remotely.
        """
        return self._run(
            action="list_session",
            ssm_client=ssm_client,
            server=server,
        )

    def stop_server(
        self,
        ssm_client: T.Optional["SSMClient"] = None,
        server: T.Optional[Server] = None,
    ):
        """
        Run :meth:`acore_server_bootstrap.cli.main.Command.stop_server` remotely.
        """
        return self._run(
            action="stop_server",
            ssm_client=ssm_client,
            server=server,
        )

    def install(
        self,
        ssm_client: T.Optional["SSMClient"] = None,
        server: T.Optional[Server] = None,
        python_version: str = "3.11",
        acore_soap_app_version: T.Optional[str] = None,
        acore_db_app_version: T.Optional[str] = None,
        acore_server_bootstrap_version: T.Optional[str] = None,
    ):
        """
        Run :ref:`bootstrap-on-first-launch-ec2` remotely.
        """
        if ssm_client is None:
            ssm_client = self.ssm_client
        if server is None:
            server = self.server
        command = server.build_bootstrap_command(
            python_version=python_version,
            acore_soap_app_version=acore_soap_app_version,
            acore_db_app_version=acore_db_app_version,
            acore_server_bootstrap_version=acore_server_bootstrap_version,
        )
        print("------ send command ------")
        print(command)
        command_invocation_list = run_shell_script_sync(
            ssm_client=ssm_client,
            commands=command,
            instance_ids=server.metadata.ec2_inst.id,
            delays=5,
            timeout=180,
            raises=False,
        )
        print("")
        command_invocation = command_invocation_list[0]
        stdout = command_invocation.StandardOutputContent.strip()
        stderr = command_invocation.StandardErrorContent.strip()
        if stdout:
            print("------ standard output ------")
            print(stdout)
        if stderr:
            print("------ ❌ standard error ------")
            print(stderr)

        return command_invocation
