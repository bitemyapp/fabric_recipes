from fabric.api import *
from fabric.colors import red, green
from fabric.utils import puts
from fabric.contrib.files import append

from cuisine import dir_ensure, file_exists, file_link, mode_sudo, \
     package_ensure_apt, user_ensure

from jinja2 import Template

root = "/srv/"
jvm_args = "-Xmx2g -Xms2g"

def root_dir():
    return root

def app_dir(name):
    return root_dir() + name

def log_dir():
    return root_dir() + "log/"

def app_log_dir(name):
    return log_dir() + name

def provision_clojure():
    """For getting a machine ready to run Clojure"""
    append("/etc/apt/sources.list.d/oracle_java.list",
           "deb http://www.duinsoft.nl/pkg debs all", use_sudo=True)
    if not file_exists("/usr/bin/java"):
        sudo("apt-key adv --keyserver keys.gnupg.net --recv-keys 5CB26B26")
    map(package_ensure_apt, ["update-sun-jre", "rsync", "unzip"])

def ensure_user(user):
    """ For the application uid """
    user_ensure(user)

def push_env(app_name):
    puts(green("Pushing environment config"))
    put("templates/clojure.env", app_dir(app_name) + "/env.sh", use_sudo=True)

def render_init(app_name):
    return Template(open("templates/clojure.init").read()).render(app_name=app_name, jvm_args=jvm_args)

def push_init(app_name):
    puts(green("Pushing init files"))
    append("/etc/init/" + app_name + ".conf", render_init(app_name), use_sudo=True)
    puts(green("Reloading init"))
    sudo("initctl reload-configuration")

def service_verb(name, verb)
    """ start, stop, restart """
    sudo("service " + name + " " + verb)

def restart_service(name)
    service_verb(name, "restart")

def push_clojure(app_name):
    map(dir_ensure, [root_dir(), app_dir(app_name), log_dir(), app_log_dir(app_name)])
    puts(green("Doing a fresh compile of your application"))
    local("lein clean && lein uberjar")
    puts(green("Pushing uberjar"))
    put("target/*standalone.jar", app_dir(), use_sudo=True)
    push_init(app_name)
    push_env(app_name)
    restart_service(app_name)
    puts(green("Restarted app, all done!"))
