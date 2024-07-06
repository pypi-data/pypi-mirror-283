.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


1.1.1 (2024-07-05)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add ``acorebs sync_lua_scripts`` bootstrap command.


1.0.1 (2024-06-22)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This version is NOT a backward in-compatible release.

**Features and Improvements**

- Add ``Remoter`` to allow run bootstrap remotely.
- Supported bootstrap command:
    - ``acorebs hello``
    - ``acorebs bootstrap_as_sudo``
    - ``acorebs bootstrap``
    - ``acorebs disable_ubuntu_auto_upgrade``
    - ``acorebs setup_ec2_run_on_restart_script``
    - ``acorebs create_database``
    - ``acorebs create_user``
    - ``acorebs update_realmlist``
    - ``acorebs configure_db``
    - ``acorebs apply_authserver_conf``
    - ``acorebs apply_worldserver_conf``
    - ``acorebs apply_mod_lua_engine_conf``
    - ``acorebs apply_server_config``
    - ``acorebs run_check_server_status_cron_job``
    - ``acorebs stop_check_server_status_cron_job``
    - ``acorebs run_server``
    - ``acorebs list_session``
    - ``acorebs enter_worldserver``
    - ``acorebs stop_server``

**Minor Improvements**

- Rework the documentation website


0.4.2 (2023-07-18)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- add more bootstrap logging to file.


0.4.1 (2023-07-17)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Automatically configure `acore_db_app <https://github.com/MacHu-GWU/acore_db_app-project>`_ project and CLI agent.


0.3.1 (2023-06-27)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Automatically launch the server status monitor cron job. It writes the server status to EC2 tag every 30 seconds.
- Add run-on-restart script to automatically restart necessary cron job and the server after reboot.

**Minor Improvements**

- refactor the code to make it more readable.
- ensure the ``sudo`` command is used when necessary.
- ensure the ``sudo -H -u ubuntu`` command is used when necessary.


0.2.1 (2023-06-19)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Automatically configure `acore_soap_app <https://github.com/MacHu-GWU/acore_soap_app-project>`_ SOAP agent.


0.1.1 (2023-06-19)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- First release
- Add ``acorebs`` command line interface.

.. code-block:: bash

    NAME
        acorebs - acore server bootstrap command line interface.


    SYNOPSIS
        acorebs COMMAND

    DESCRIPTION
        acore server bootstrap command line interface.


    COMMANDS
        COMMAND is one of the following:

         info
           Print welcome message.

         bootstrap
           Bootstrap a new EC2 server.

         apply_authserver_conf
           Update the authserver.conf.

         apply_worldserver_conf
           Update the worldserver.conf.

         apply_mod_lua_engine_conf
           Update the mod_LuaEngine.conf.

         apply_server_config
           Update the authserver.conf, worldserver.conf and mod_LuaEngine.conf.

         create_database
           Create the database user for game server and three initial databases.

         create_user
           Create the database user for game server.

         update_realmlist
           Update 'acore_auth.realmlist.address'.

         configure_db
           Configure the database for game server.

         disable_ubuntu_auto_upgrade
           Disable Ubuntu auto upgrade (don't upgrade mysql).

         run_server
           Run the game server in screen session.

         list_session
           List all screen sessions.

         enter_worldserver
           Enter the worldserver screen session.

         stop_server
           Stop the game server.
