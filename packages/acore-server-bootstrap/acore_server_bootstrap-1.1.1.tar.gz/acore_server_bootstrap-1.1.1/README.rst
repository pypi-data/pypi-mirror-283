.. image:: https://readthedocs.org/projects/acore-server-bootstrap/badge/?version=latest
    :target: https://acore-server-bootstrap.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/acore_server_bootstrap-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/acore_server_bootstrap-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/acore_server_bootstrap-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/acore_server_bootstrap-project

.. image:: https://img.shields.io/pypi/v/acore-server-bootstrap.svg
    :target: https://pypi.python.org/pypi/acore-server-bootstrap

.. image:: https://img.shields.io/pypi/l/acore-server-bootstrap.svg
    :target: https://pypi.python.org/pypi/acore-server-bootstrap

.. image:: https://img.shields.io/pypi/pyversions/acore-server-bootstrap.svg
    :target: https://pypi.python.org/pypi/acore-server-bootstrap

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/acore_server_bootstrap-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/acore_server_bootstrap-project

.. image:: https://img.shields.io/badge/Acore_Doc--None.svg?style=social&logo=readthedocs
    :target: https://acore-doc.readthedocs.io/en/latest/

------

.. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://acore-server-bootstrap.readthedocs.io/en/latest/

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://acore-server-bootstrap.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/acore_server_bootstrap-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/acore_server_bootstrap-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/acore_server_bootstrap-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/acore-server-bootstrap#files


Welcome to ``acore_server_bootstrap`` Documentation
==============================================================================
.. image:: https://acore-server-bootstrap.readthedocs.io/en/latest/_static/acore_server_bootstrap-logo.png
    :target: https://acore-server-bootstrap.readthedocs.io/en/latest/

**项目背景**

在大规模游戏服务器 (Azerothcore) 部署的流程中, 我们通常会将其分为以下几个步骤:

1. 游戏服务器核心的编译.
2. 将编译好的游戏服务器打包成镜像.
3. 对用镜像启动的游戏服务器进行自动配置.

而 #3 这一步又可以分为以下几个步骤:

1. 创建数据库的 user.
2. 创建三个数据库 (auth, characters, world), 如果还没创建过的话.
3. 将必要的配置写入数据中 (realmlist).
4. 将最新的配置写入 ``*.conf`` 文件中.
5. 禁止 ubuntu 的自动升级.
6. 对游戏服务器的启动脚本赋予可执行权限.
7. 启动游戏服务器.
8. 安装其他服务器组件, 例如 SOAP Agent, DB Agent 等.

这一连串步骤在每次开新服, 或是修改了配置文件的时候都需要进行, 非常的麻烦. 为了解决这个问题, 我们开发了 ``acore_server_bootstrap`` 这个工具, 它可以帮助我们自动完成上述的所有步骤.

**Note**

    注意, 该工具假设服务器的文件目录严格遵循了 `acore_paths <https://github.com/MacHu-GWU/acore_paths-project>`_ 项目中的定义. 如果该假设不满足, 则无法使用该工具. 例如我们构建的服务器核心要在 ``/home/ubuntu/azeroth-server`` 目录下.

**Document**

如果想详细了解 bootstrap 的原理和所有命令的细节, 请阅读 `How bootstrap works <https://acore-server-bootstrap.readthedocs.io/en/latest/search.html?q=How+Bootstrap+Works&check_keywords=yes&area=default>`_

**Cheat Sheet**

如果你已经熟悉了 bootstrap 的原理, 可以直接查看 `Cheat Sheet <https://acore-server-bootstrap.readthedocs.io/en/latest/search.html?q=Cheat+Sheet&check_keywords=yes&area=default>`_ 来查看所有命令的用法.


.. _install:

Install
------------------------------------------------------------------------------

``acore_server_bootstrap`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install acore-server-bootstrap

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade acore-server-bootstrap
