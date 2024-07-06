# -*- coding: utf-8 -*-

"""
todo: add docstring
"""

import subprocess

from light_emoji import common

from ...logger import logger
from ...logger_root import get_logger

from .paths import (
    path_20auto_upgrade_source,
    path_20auto_upgrade_target,
    path_wserver_run_on_restart_sh_source,
    path_wserver_run_on_restart_sh_target,
)


@logger.start_and_end(msg="{func_name}")
def disable_ubuntu_auto_upgrade():
    """
    关闭 Ubuntu 的自动更新. 主要是为了防止 Ubuntu 更新 MySQL Client 的小版本. 因为游戏服务器
    要求 MySQL Client 的版本跟服务器编译时的版本一摸一样 (数据库的版本可以比核心和 MySQL client 高).

    **如何判断 Auto Upgrade 是否已经被禁用**

    .. code-block:: bash

        cat /etc/apt/apt.conf.d/20auto-upgrades

    如果你看到了如下内容, 说明 **自动升级没有被禁用**

    .. code-block::

        APT::Periodic::Update-Package-Lists "1";
        APT::Periodic::Unattended-Upgrade "1";

    如果你看到了如下内容, 说明 **自动升级已经被禁用**

    .. code-block::

        APT::Periodic::Update-Package-Lists "0";
        APT::Periodic::Unattended-Upgrade "0";

    Reference:

    - https://askubuntu.com/questions/1322292/how-do-i-turn-off-automatic-updates-completely-and-for-real
    """
    file_logger = get_logger()
    file_logger.debug(
        f"{common.play_or_pause} disable ubuntu auto upgrade, this step requires sudo"
    )
    file_logger.debug(
        f"copy {path_20auto_upgrade_source} to {path_20auto_upgrade_target}"
    )
    logger.info(f"Apply changes to {path_20auto_upgrade_target}")

    args = [
        "sudo",
        "cp",
        f"{path_20auto_upgrade_source}",
        f"{path_20auto_upgrade_target}",
    ]
    subprocess.run(args, check=True)


@logger.start_and_end(msg="{func_name}")
def setup_ec2_run_on_restart_script():
    """
    EC2 可以用 User Data 来指定在第一次 Launch EC2 的时候运行一些自动化脚本来配置机器.
    但是这只限于第一次 Launch. 作为游戏服务器, 我们是有一些自动化脚本需要在每次重启时运行的.
    这里我们使用了 AWS 官方提议的方法, 将我们需要运行的自动化脚本放到
    ``/var/lib/cloud/scripts/per-boot/`` 目录下. 这样每次重启的时候, 这个目录下的脚本都会被
    ``cloud-init`` 这个每个 EC2 都会自动运行的启动程序所运行. 值得注意的是, 默认该目录下
    的脚本会以 root 用户的身份运行, 而如果你的脚本需要创建一些给 ubuntu 用户使用的文件, 那么
    就要注意用 ``sudo -H -u ubuntu ...`` 命令来切换用户了.

    这里有三个文件比较重要:

    - ``wserver-run-on-restart.sh``: 这个脚本要被放到 ``/var/lib/cloud/scripts/per-boot/``
        目录下, 也是每次启动时要运行的自动化脚本. 注, 该脚本在 EC2 第一次 Launch 的时候不存在,
        而是会由 User Data 中的脚本来创建.
    - ``wserver_run_on_restart.py``: 这个脚本会被 ``wserver-run-on-restart.sh`` 所调用,
        用来执行不需要 sudo 权限的任务.
    - ``wserver_run_on_restart_as_sudo.py``: 这个脚本也会被 ``wserver-run-on-restart.sh``
        所调用,用来执行不需要 sudo 权限的任务.

    Reference:

    - Run commands on your Linux instance at launch: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html
    - How can I utilize user data to automatically run a script with every restart of my Amazon EC2 Linux instance?: https://repost.aws/knowledge-center/execute-user-data-ec2
    """
    file_logger = get_logger()
    file_logger.debug(
        f"{common.play_or_pause} setup ec2 run on restart script, this step requires sudo"
    )
    file_logger.debug(
        f"copy {path_wserver_run_on_restart_sh_source} to {path_wserver_run_on_restart_sh_target}"
    )
    logger.info(f"Create / update {path_wserver_run_on_restart_sh_target}")
    args = [
        f"sudo",
        "cp",
        f"{path_wserver_run_on_restart_sh_source}",
        f"{path_wserver_run_on_restart_sh_target}",
    ]
    subprocess.run(args)

    file_logger.debug(
        f"Change mode to executable for {path_wserver_run_on_restart_sh_target}"
    )
    logger.info(f"Change mode to executable")
    args = [
        f"sudo",
        "chmod",
        "777",  # +x is just for the file owner, +777 is for everyone
        f"{path_wserver_run_on_restart_sh_target}",
    ]
    subprocess.run(args)
