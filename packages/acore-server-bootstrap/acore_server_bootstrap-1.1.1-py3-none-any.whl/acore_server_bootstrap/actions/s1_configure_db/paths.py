# -*- coding: utf-8 -*-

from pathlib_mate import Path

_dir_here = Path.dir_here(__file__)

dir_create = _dir_here / "create"

path_create_mysql_database_aws_rds_sql_template = dir_create / "create_mysql_database.sql.aws_rds_mode.jinja2"
path_create_mysql_user_aws_rds_sql_template = dir_create / "create_mysql_user.sql.aws_rds_mode.jinja2"
path_update_realmlist_address_sql_template = dir_create / "update_realmlist_address.sql.jinja2"

path_create_mysql_database = dir_create / "create_mysql_database.sql"
path_create_mysql_user = dir_create / "create_mysql_user.sql"
path_update_realmlist_address = dir_create / "update_realmlist_address.sql"
