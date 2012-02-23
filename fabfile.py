# -*- coding: utf-8 -*-

import os

from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.files import upload_template, exists
from fabric.operations import require
from fabric.utils import warn

env.hosts = ['ec2-107-21-102-210.compute-1.amazonaws.com']
env.directory = '/home/www/projects/uralsocionics'
env.deploy_user = 'www'

def virtualenv(command):
    with cd(env.directory):
        sudo(env.activate + '&&' + command, user=env.deploy_user)


@hosts('ec2-107-21-102-210.compute-1.amazonaws.com')
def production():
    upload()
    packages()
    set_lighttpd()
    dump()
    migrate()
    restart()


def upload():
    pass


def packages():
    virtualenv('pip install -r requirements.txt')


def set_lighttpd():
    with cd(env.directory):
        sudo('cp tools/lighttpd/90-uralsocionics.conf /etc/lighttpd/conf-available/90-uralsocionics.conf')
        sudo('ln -s /etc/lighttpd/conf-available/90-uralsocionics.conf /etc/lighttpd/conf-enabled/90-uralsocionics.conf')
        sudo('/etc/init.d/lighttpd restart')


def dump():
    pass


def migrate():
    with cd(env.directory):
        run('ENV/bin/python src/manage.py migrate')


def restart():
    sudo('sv restart uralsocionics')