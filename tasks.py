from invoke import task
from fabric import Connection


@task
def add_user(context, admin_name, password):
    APP_USER = 'srt'
    """ Creates app user if it does not exist. """
    print('Looking for {} user...'.format(APP_USER))
    conn = Connection('94.130.5.230', user=admin_name, connect_kwargs={'password': password})
    result = conn.sudo('test -d /home/{}'.format(APP_USER), warn=True, password=password)
    if not result.failed:
        print('{} home directory found. Do nothing.'.format(APP_USER))
    else:
        print('{} home directory was not found. Creating {} user...'.format(APP_USER, APP_USER))
        conn.sudo('adduser {} --disabled-login --disabled-password --gecos ""'.format(APP_USER), password=password)
        print('{} user created.'.format(APP_USER))

    # Ensure app dir exists.
    conn.run('mkdir -p ~/app')


def get_release_name(context):
    result = context.run('git rev-parse HEAD')
    commit_hash = result.stdout[:8]
    return 'srt_web_app_%s' % commit_hash


@task
def put_app(context, conn):
    # Create release archive.
    archive_name = get_release_name(context) + '.zip'
    # directory change.
    # with context.cd('../'):
    #    ...
    context.run(
        'git archive --format=zip HEAD > {}'.format(archive_name))

    # Send archive to remote side.
    conn.put(archive_name, '/tmp')

    # Unzip on remote side.
    # Ensure ~/app exists.
    conn.run('mkdir -p ~/app')
    conn.run('unzip -o /tmp/{} -d {}'.format(archive_name, '~/app/'))


def supervisor_conf(password, conn):
    conn.sudo('cp app/admin/etc/supervisor/conf.d/srt_app.conf /etc/supervisor/conf.d/', password=password)
    conn.sudo('supervisorctl reread', password=password)
    conn.sudo('supervisorctl update', password=password)


def nginx_conf(password, conn):
    conn.sudo('cp app/admin/etc/nginx/sites-available/srt_app /etc/nginx/sites-available/srt_app', password=password)
    result = conn.sudo('test -f /etc/nginx/sites-enabled/srt_app', warn=True, password=password)
    if result.failed:
        conn.sudo('ln -s /etc/nginx/sites-available/srt_app /etc/nginx/sites-enabled/', password=password)
        conn.sudo('systemctl restart nginx', password=password)
    else:
        conn.sudo('systemctl restart nginx', password=password)


@task
def basic_deploy(context, admin_name, password):
    conn = Connection('94.130.5.230', user=admin_name, connect_kwargs={'password': password})
    put_app(context, conn)
    supervisor_conf(password, conn)
    nginx_conf(password, conn)
