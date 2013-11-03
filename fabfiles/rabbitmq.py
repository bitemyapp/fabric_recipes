from fabric.api import *
from cuisine import dir_ensure, file_exists, file_link, mode_sudo, \
     package_ensure_apt, user_ensure

def provision_bunny(admin_password):
    append("/etc/apt/sources.list.d/rabbitmq.list",
           "deb http://www.rabbitmq.com/debian/ testing main", use_sudo=True)
    if not file_exists("/usr/sbin/rabbitmq-server"):
        sudo("wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc")
        sudo("apt-key add rabbitmq-signing-key-public.asc")
        map(package_ensure_apt, ["rabbitmq-server", "rsync"])
        dir_ensure("/etc/rabbitmq/rabbitmq.conf.d")
        put("./conf/bunny/bunny.conf", "/etc/rabbitmq/rabbitmq.conf.d/", use_sudo=True)
        sudo("chown -R rabbitmq.rabbitmq /srv/rabbitmq")
        dir_ensure("/srv/rabbitmq/log", owner="rabbitmq", group="rabbitmq")
        sudo("rm -rf /var/lib/rabbitmq")
        sudo("rm -rf /var/log/rabbitmq")
        with mode_sudo():
            file_link("/srv/rabbitmq", "/var/lib/rabbitmq", owner="rabbitmq", group="rabbitmq")
            file_link("/srv/rabbitmq/log", "/var/log/rabbitmq", owner="rabbitmq", group="rabbitmq")
        sudo("service rabbitmq-server start")
        sudo("rabbitmq-plugins enable rabbitmq_management")
        sudo("rabbitmqctl add_user admin " + admin_password)
        sudo("rabbitmqctl set_user_tags admin administrator")
        sudo('rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"')
        sudo("rabbitmqctl delete_user guest")
        sudo("service rabbitmq-server restart")
    else:
        print "skipped install, already have /usr/sbin/rabbitmq-server"
