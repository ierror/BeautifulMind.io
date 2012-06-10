# -*- coding: utf-8 -*-
from fabric.api import env, roles, run, sudo
from fabric.contrib import files


REMOTE_REPO_PATH = '/opt/beautifulmind/www/'
REMOTE_PROJECT_PATH = REMOTE_REPO_PATH+'beautifulmind/'

env.user = 'root'

# Define sets of servers as roles
env.roledefs = {
    'production_web': ['app-1.beautifulmind.io'],
}

@roles('production_web')
def deploy_production_web():
    def _sudo(command, *args, **kwargs):
        command = 'source %svirtualenv/bin/activate && %s' % (REMOTE_PROJECT_PATH, command)
        sudo(command, user='www-data', *args, **kwargs)

    def manage_py(command):
        _sudo('python %smanage.py %s' % (REMOTE_PROJECT_PATH, command))

    # stop services
    run('supervisorctl stop mindmaptornado')
    run('supervisorctl stop uwsgi')

    # backup
    _sudo('%sdeployment/db_backup.sh' % (REMOTE_PROJECT_PATH))
    _sudo('cd %s; git reset --hard production && git pull' % (REMOTE_PROJECT_PATH))

    # install python modules
    _sudo('cd %s; source virtualenv/bin/activate; pip install -r REQUIREMENTS' % (REMOTE_PROJECT_PATH))

    _sudo('rm -rf %sassets/static/' % (REMOTE_PROJECT_PATH))
    manage_py('collectstatic --noinput')

    # run missing migrations
    manage_py('migrate')

    # force DEBUG = False
    files.sed('%ssettings.py' % (REMOTE_PROJECT_PATH), '^DEBUG\s*=\s*True$', 'DEBUG = False')

    # rm pyc files
    manage_py('clean_pyc')

    # start services
    run('supervisorctl start mindmaptornado')
    run('supervisorctl start uwsgi')
