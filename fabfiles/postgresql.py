from fabric.api import *
from cuisine import dir_ensure, file_exists, file_link, mode_sudo, \
     package_ensure_apt, user_ensure

def provision_postgresql():
    package_ensure_apt("postgresql")

def ensure_role(username, password):
    postgresql_role_ensure(username, password, createdb=True)

def ensure_database(db_name, owner):
    # owner should == what you used in ensure_role
    postgresql_database_ensure(db_name, owner=owner, encoding="UTF8")
