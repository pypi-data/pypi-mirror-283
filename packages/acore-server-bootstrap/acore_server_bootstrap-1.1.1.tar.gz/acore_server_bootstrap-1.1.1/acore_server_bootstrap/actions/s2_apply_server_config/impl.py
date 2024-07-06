# -*- coding: utf-8 -*-

"""
todo: add docstring
"""

import subprocess
from pathlib_mate import Path

import acore_paths.api as acore_paths
from acore_conf.api import apply_changes
from acore_server.api import Server

from light_emoji import common

from ...logger import logger
from ...logger_ubuntu import get_logger


@logger.start_and_end(msg="{func_name}")
def apply_authserver_conf(server: Server):
    """
    从 S3 上拉取 configuration 数据, 并把
    `acore_server_config.api.Server.authserver_conf <https://acore-server-config.readthedocs.io/en/latest/acore_server_config/config/define/server.html#acore_server_config.config.define.server.Server>`_
    中的数据应用到 ``authserver.conf`` 文件中.
    """
    file_logger = get_logger()
    file_logger.debug(f"{common.play_or_pause} apply authserver config ...")
    data = server.config.authserver_conf.copy()
    data.update(
        {
            "LoginDatabaseInfo": f"{server.metadata.rds_inst.endpoint};3306;{server.config.db_username};{server.config.db_password};acore_auth",
        }
    )
    logger.info(
        f"copy from template: {acore_paths.path_azeroth_server_authserver_conf_dist}"
    )
    logger.info(f"create: {acore_paths.path_azeroth_server_authserver_conf}")
    apply_changes(
        path_input=acore_paths.path_azeroth_server_authserver_conf_dist,
        path_output=acore_paths.path_azeroth_server_authserver_conf,
        data={"authserver": data},
    )


@logger.start_and_end(msg="{func_name}")
def apply_worldserver_conf(server: Server):
    """
    从 S3 上拉取 configuration 数据, 并把
    `acore_server_config.api.Server.worldserver_conf <https://acore-server-config.readthedocs.io/en/latest/acore_server_config/config/define/server.html#acore_server_config.config.define.server.Server>`_
    中的数据应用到 ``worldserver.conf`` 文件中.
    """
    file_logger = get_logger()
    file_logger.debug(f"{common.play_or_pause} apply worldserver config ...")
    data = server.config.worldserver_conf.copy()
    data.update(
        {
            "DataDir": f"{acore_paths.dir_azeroth_server_data}",
            "LogsDir": f"{acore_paths.dir_azeroth_server_logs}",
            "LoginDatabaseInfo": f"{server.metadata.rds_inst.endpoint};3306;{server.config.db_username};{server.config.db_password};acore_auth",
            "WorldDatabaseInfo": f"{server.metadata.rds_inst.endpoint};3306;{server.config.db_username};{server.config.db_password};acore_world",
            "CharacterDatabaseInfo": f"{server.metadata.rds_inst.endpoint};3306;{server.config.db_username};{server.config.db_password};acore_characters",
        }
    )
    logger.info(
        f"copy from template: {acore_paths.path_azeroth_server_worldserver_conf_dist}"
    )
    logger.info(f"create: {acore_paths.path_azeroth_server_worldserver_conf}")
    apply_changes(
        path_input=acore_paths.path_azeroth_server_worldserver_conf_dist,
        path_output=acore_paths.path_azeroth_server_worldserver_conf,
        data={"worldserver": data},
    )


@logger.start_and_end(msg="{func_name}")
def apply_mod_lua_engine_conf(server: Server):
    """
    从 S3 上拉取 configuration 数据, 并把
    `acore_server_config.api.Server.mod_lua_engine_conf <https://acore-server-config.readthedocs.io/en/latest/acore_server_config/config/define/server.html#acore_server_config.config.define.server.Server>`_
    中的数据应用到 ``mod_LuaEngine.conf`` 文件中.
    """
    file_logger = get_logger()
    file_logger.debug(f"{common.play_or_pause} apply mod lua engine config ...")
    data = server.config.mod_lua_engine_conf.copy()
    data.update(
        {
            "Eluna.ScriptPath": f"{acore_paths.dir_server_lua_scripts}",
        }
    )
    logger.info(f"copy from template: {acore_paths.path_mod_eluna_conf_dist}")
    logger.info(f"create: {acore_paths.path_mod_eluna_conf}")
    apply_changes(
        path_input=acore_paths.path_mod_eluna_conf_dist,
        path_output=acore_paths.path_mod_eluna_conf,
        data={"worldserver": data},
    )


@logger.start_and_end(msg="{func_name}")
def apply_server_config(server: Server):
    """
    Run the following functions:

    - :func:`apply_authserver_conf`
    - :func:`apply_worldserver_conf`
    - :func:`apply_mod_lua_engine_conf`
    """
    file_logger = get_logger()
    file_logger.debug(f"{common.play_or_pause} apply server config ...")
    with logger.nested():
        apply_authserver_conf(server)
        apply_worldserver_conf(server)
        apply_mod_lua_engine_conf(server)


@logger.start_and_end(msg="{func_name}")
def sync_lua_scripts(
    s3dir_uri: str,
):
    """
    清空本地的 lua_scripts 中的所有 lua 文件, 然后从指定的 S3 dir 中下载所有的 lua 文件到本地.
    """
    dir_server_lua_scripts = Path(acore_paths.dir_server_lua_scripts)
    for path in dir_server_lua_scripts.select_by_ext(".lua"):
        path.remove()
    args = [
        "/home/ubuntu/.pyenv/shims/aws",
        "s3",
        "sync",
        s3dir_uri,
        str(dir_server_lua_scripts),
    ]
    subprocess.run(args, check=True)
