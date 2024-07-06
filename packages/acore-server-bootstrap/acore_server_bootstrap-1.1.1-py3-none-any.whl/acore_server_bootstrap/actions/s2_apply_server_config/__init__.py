# -*- coding: utf-8 -*-

"""
这一步是将游戏服务器的 authserver, worldserver 以及所有模组的配置文件数据从 S3 上拉取下来
并覆盖对应的文件. 这样之后每次启动游戏都是用的最新的配置启动的. 这一步也是幂等的.

.. note::

    这一步不能用 root 来执行, 而必须用 ubuntu 用户来执行. 因为如果用 root 来执行, 那么
    自动生成的 ``~/azeroth-server/etc/worldserver.conf`` 文件就只能被 root 来读取, 而
    我们一般是用 ubuntu 用户来启动游戏服务器的.
"""