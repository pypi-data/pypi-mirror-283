# -*- coding: utf-8 -*-

"""
todo: add docstring
"""

import typing as T
import subprocess
from jinja2 import Template
from pathlib_mate import Path

from light_emoji import common
from acore_server.api import Server

from ...logger import logger
from ...logger_ubuntu import get_logger

from .paths import (
    path_create_mysql_database_aws_rds_sql_template,
    path_create_mysql_user_aws_rds_sql_template,
    path_update_realmlist_address_sql_template,
)


# ------------------------------------------------------------------------------
# low level api
# ------------------------------------------------------------------------------
def run_sql(
    sql: str,
    host: str,
    database: T.Optional[str] = None,
    username: T.Optional[str] = None,
    password: T.Optional[str] = None,
    timeout: T.Optional[int] = None,
    path: Path = Path.home().joinpath("tmp.sql"),
):
    """
    Run a SQL statement via MySQL cli.

    一个调用 MySQL cli 来运行大段 SQL 的函数. 本质上是 CLI 命令的封装
    """
    args = [
        "sudo",
        "mysql",
        f"--host={host}",
    ]
    if database:
        args.append(f"--database={database}")
    if username:
        args.append(f"--user={username}")
        args.append(f"--password={password}")
    if timeout:
        args.append(f"--connect-timeout={timeout}")
    path.write_text(sql)
    with path.open("r") as f:
        subprocess.run(args, stdin=f, text=True)


def render_create_mysql_database_sql_in_rds_mode(
    database_username: str,
    database_password: str,
) -> str:
    """
    Return the SQL statement that can create Azerothcore Database user and
    initial databases, and grant new user Database permission.
    """
    template = Template(path_create_mysql_database_aws_rds_sql_template.read_text())
    return template.render(
        database_username=database_username,
        database_password=database_password,
    )


def render_create_mysql_user_sql_in_rds_mode(
    database_username: str,
    database_password: str,
) -> str:
    """
    Return the SQL statement that can create Azerothcore Database user and
    grant new Database permission (without creating the database).
    """
    template = Template(path_create_mysql_user_aws_rds_sql_template.read_text())
    return template.render(
        database_username=database_username,
        database_password=database_password,
    )


def run_create_mysql_database_sql_in_rds_mode(
    database_username: str,
    database_password: str,
    database_host: str,
    database_admin_username: str = None,
    database_admin_password: str = None,
):
    """
    为游戏服务器创建数据库 User 账号密码. 并创建三个空数据库.

    :param database_username: 给游戏服务器用的 DB User 账号, 默认是 acore
    :param database_password: 给游戏服务器用的 DB User 密码
    :param database_host: RDS Instance 的 Endpoint (不包括 port)
    :param database_admin_username: RDS Instance 的 master username 默认是 admin
        这是你创建 RDS 的时候的 admin 账号, 不是给游戏服务器用的 acore 那个.
    :param database_admin_password: RDS Instance 的 master password
        这是你创建 RDS 的时候的 admin 密码, 不是给游戏服务器用的 acore 那个.
    """
    sql = render_create_mysql_database_sql_in_rds_mode(
        database_username=database_username,
        database_password=database_password,
    )
    run_sql(
        sql=sql,
        host=database_host,
        username=database_admin_username,
        password=database_admin_password,
        timeout=3,
    )


def run_create_mysql_user_sql_in_rds_mode(
    database_username: str,
    database_password: str,
    database_host: str,
    database_admin_username: str = None,
    database_admin_password: str = None,
):
    """
    更新给游戏服务器用的数据库 User 账号密码. 常用于密码更改时对已经存在的 EC2 进行重新配置.

    :param database_username: 给游戏服务器用的 DB User 账号, 默认是 acore
    :param database_password: 给游戏服务器用的 DB User 密码
    :param database_host: RDS Instance 的 Endpoint (不包括 port)
    :param database_admin_username: RDS Instance 的 master username 默认是 admin
        这是你创建 RDS 的时候的 admin 账号, 不是给游戏服务器用的 acore 那个.
    :param database_admin_password: RDS Instance 的 master password
        这是你创建 RDS 的时候的 admin 密码, 不是给游戏服务器用的 acore 那个.
    """
    sql = render_create_mysql_user_sql_in_rds_mode(
        database_username=database_username,
        database_password=database_password,
    )
    run_sql(
        sql=sql,
        host=database_host,
        username=database_admin_username,
        password=database_admin_password,
        timeout=3,
    )


def render_update_realmlist_address_sql(server_public_ip: str) -> str:
    """
    Return the SQL statement that can update the realmlist address.
    """
    template = Template(path_update_realmlist_address_sql_template.read_text())
    return template.render(
        server_public_ip=server_public_ip,
    )


def run_update_realmlist_address_sql(
    server_public_ip: str,
    database_host: str,
    database_admin_username: str = None,
    database_admin_password: str = None,
):
    """
    更新 acore_auth.realmlist 表里面的 address 字段. 从而让登录服务器知道如何路由到游戏服务器.

    :param server_public_ip: EC2 的公网 IP 地址
    :param database_host: RDS Instance 的 Endpoint (不包括 port)
    :param database_admin_username: RDS Instance 的 master username 默认是 admin
        这是你创建 RDS 的时候的 admin 账号, 不是给游戏服务器用的 acore 那个.
    :param database_admin_password: RDS Instance 的 master password
        这是你创建 RDS 的时候的 admin 密码, 不是给游戏服务器用的 acore 那个.
    """
    sql = render_update_realmlist_address_sql(
        server_public_ip=server_public_ip,
    )
    run_sql(
        sql=sql,
        host=database_host,
        database="acore_auth",
        username=database_admin_username,
        password=database_admin_password,
        timeout=3,
    )


# ------------------------------------------------------------------------------
# high level api
# ------------------------------------------------------------------------------
@logger.start_and_end(msg="{func_name}")
def create_database(server: Server):
    """
    在第一次开服的时候, 游戏数据库中是没有 ``acore_auth``, ``acore_characters``,
    ``acore_world`` 三个数据库的, 我们需要创建他们. 这个函数是幂等的, 也就是说如果某一个数据库已经
    存在了, 那么这个函数会跳过这个数据库的创建.
    """
    file_logger = get_logger()
    file_logger.debug(
        f"{common.play_or_pause} Create database user for game server ..."
    )
    file_logger.debug(
        "Create three database acore_auth, acore_characters, acore_world ..."
    )
    logger.info("Create database user for game server ...")
    logger.info("Create three database acore_auth, acore_characters, acore_world ...")
    run_create_mysql_database_sql_in_rds_mode(
        database_username=server.config.db_username,
        database_password=server.config.db_password,
        database_host=server.metadata.rds_inst.endpoint,
        database_admin_username="admin",
        database_admin_password=server.config.db_admin_password,
    )


@logger.start_and_end(msg="{func_name}")
def create_user(server: Server):
    """
    游戏服务器连接数据库不是用的 Admin User (这样安全隐患太大了), 而是用我们创建的 Acore DB User.
    在第一次开服的时候我们需要创建这些 User 并且给它们对应的 database 的访问权限.
    并且, 如果我们修改了 configuration, 其中就包含了数据库用户名和密码, 我们同样要删掉
    旧的 DB User 并重新配置. 这个任务就是做这件事的.
    """
    logger.info("Create database user for game server ...")
    run_create_mysql_user_sql_in_rds_mode(
        database_username=server.config.db_username,
        database_password=server.config.db_password,
        database_host=server.metadata.rds_inst.endpoint,
        database_admin_username="admin",
        database_admin_password=server.config.db_admin_password,
    )


@logger.start_and_end(msg="{func_name}")
def update_realmlist(server: Server):
    """
    在 ``acore_auth.realmlist`` 表中我们需要设定我们的游戏服务器的 IP. 这样登录服务器鉴权成功后
    才能将游戏客户端的连接导向到我们的游戏服务器. 而由于我们的 IP 地址可能在 EC2 重启后发生变化,
    所以我们需要在每次重启 EC2 后更新这个表.
    """
    file_logger = get_logger()
    file_logger.debug(f"{common.play_or_pause} Update acore_auth.realmlist.address ...")
    logger.info("Update acore_auth.realmlist.address ...")
    run_update_realmlist_address_sql(
        server_public_ip=server.metadata.ec2_inst.public_ip,
        database_host=server.metadata.rds_inst.endpoint,
        database_admin_username="admin",
        database_admin_password=server.config.db_admin_password,
    )


@logger.start_and_end(msg="{func_name}")
def configure_db(server: Server):
    """
    你需要为游戏服务器创建数据库用户才能让游戏服务器和数据库互相认识. 每次启动 EC2 游戏服务器时,
    如果不是在生产环境, IP 地址还可能会变, 导致我们需要更新 realmlist.address 字段的值.
    这一步可以自动化配置跟数据库相关的操作.

    See:

    - :func:`create_database`
    - :func:`update_realmlist`
    """
    file_logger = get_logger()
    file_logger.debug(f"{common.play_or_pause} configure database ...")
    with logger.nested():
        create_database(server)
        update_realmlist(server)
