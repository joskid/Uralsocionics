# -*- coding: utf-8 -*-

import os

from fabric.api import *
from fabric.contrib.files import exists, sed, upload_template

from fab_settings import *

env.hosts = ['ec2-107-21-102-210.compute-1.amazonaws.com']
env.directory = '/home/www/projects/uralsocionics'
env.manage_dir = env.directory + '/src'
env.deploy_user = 'www'
env.user = 'www'
env.activate = 'source %s/ENV/bin/activate' % env.directory

def virtualenv(command):
    with cd(env.directory):
        run(env.activate + ' && ' + command)


@hosts('ec2-107-21-102-210.compute-1.amazonaws.com')
def init():
    packages = ('lighttpd', 'mysql-server', 'mysql-client', 'build-dep', 'python-mysqldb',
                'python-dev', 'runit', 'rrdtool', 'sendmail')
    for package in packages:
        sudo('apt-get install %s' % package)


@hosts('ec2-107-21-102-210.compute-1.amazonaws.com')
def production():
    upload()
    environment()
    local_settings()
    lighttpd()
    runit()
    dump()
    migrate()
    restart()


def upload():
    local('git archive -o archive.tar.gz HEAD')
    put('archive.tar.gz', env.directory + '/archive.tar.gz')
    with cd(env.directory):
        run('tar -zxf archive.tar.gz')
        run('rm archive.tar.gz')
    local('del archive.tar.gz')


def environment():
    with cd(env.directory):
        with settings(warn_only=True):
            run('python virtualenv.py ENV')
        virtualenv('pip install -r requirements.txt')


def local_settings():
    with cd(env.manage_dir):
        upload_template(
            'src/local_settings.py.sample',
            'local_settings.py',
            locals(),
            backup=False
        )


def lighttpd():
    sudo('cp %(directory)s/tools/lighttpd/90-uralsocionics.conf /etc/lighttpd/conf-available/90-uralsocionics.conf' % env, shell=False)
    if not exists('/etc/lighttpd/conf-enabled/90-uralsocionics.conf'):
        sudo('ln -s /etc/lighttpd/conf-available/90-uralsocionics.conf /etc/lighttpd/conf-enabled/90-uralsocionics.conf', shell=False)
#    sudo('/etc/init.d/lighttpd reload', shell=False)


def runit():
    sudo('cp %(directory)s/tools/runit/run /etc/sv/uralsocionics/run' % env, shell=False)


def dump():
    pass


def manage_py(command):
    virtualenv('cd %s && python manage.py %s' % (env.manage_dir, command))


def migrate():
    manage_py('migrate')


def restart():
    sudo('sv restart uralsocionics')