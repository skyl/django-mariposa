import subprocess
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = ''
    help = 'run mariposa migrate based on your settings'
    option_list = BaseCommand.option_list + (
        make_option('-n', '--dry-run',
                    action='store_true',
                    dest='dry-run',
                    default=False,
                    help='dry-run'),
        )

    def handle(self, *args, **options):
        # d for MARIPOSA_DIRECTORY
        d = getattr(settings, "MARIPOSA_DIRECTORY")
        if not d:
            raise CommandError('settings must specify MARIPOSA_DIRECTORY')

        default_db = settings.DATABASES['default']
        engine = default_db['ENGINE']
        # e for engine
        # c for connection string
        if 'postgres' in engine:
            e = 'postgres'
            c = ('{{"host":"{HOST}","port":"{PORT}","user":"{USER}",'
                 '"password":"{PASSWORD}","dbname":"{NAME}"}}'
            ).format(**default_db)
        elif 'sqlite' in engine:
            e = 'sqlite'
            c = default_db['NAME']
        elif 'oracle' in engine:
            e = 'oracle'
            c = "{user}/{password}@{name}".format(
                user=default_db['USER'],
                password=default_db['PASSWORD'],
                name=default_db['NAME'],
            )
        else:
            raise CommandError(
                'Could not get database engine. '
                'Only sqlite, oracle and postgres are supported.')

        cmd = [
            "mariposa",
            "migrate",
            "-c", '%s' % c,
            "-d", '%s' % d,
            "-e", e,
            "-x",  # don't create dbmigration table automatically
        ]
        if options['dry-run']:
            cmd.append('--dry-run')
        proc = subprocess.Popen(cmd, shell=False)
        proc.communicate()
        return
