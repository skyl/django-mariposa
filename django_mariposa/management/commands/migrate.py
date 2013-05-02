import subprocess
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = ''
    help = 'run mariposa migrate based on your settings'
    option_list = BaseCommand.option_list + (
        make_option('--dry-run',
                    action='store_true',
                    dest='dry-run',
                    default=False,
                    help='dry-run'),
        )

    def handle(self, *args, **options):
        d = getattr(settings, "MARIPOSA_DIRECTORY")
        if not d:
            raise CommandError('settings must specify MARIPOSA_DIRECTORY')

        default_db = settings.DATABASES['default']
        engine = default_db['ENGINE']
        if 'postgres' in engine:
            e = 'postgres'
            c = ('{{"host":"{HOST}","port":"{PORT}","user":"{USER}",'
                 '"password":"{PASSWORD}","dbname":"{NAME}"}}'
            ).format(**default_db)
        elif 'sqlite' in engine:
            e = 'sqlite'
            c = default_db['NAME']
        else:
            raise CommandError(
                'Could not get database engine. '
                'Only sqlite and postgres are supported.')

        cmd = [
            "mariposa",
            "migrate",
            "-c", '%s' % c,
            "-d", '%s' % d,
            "-e", e,
        ]
        if options['dry-run']:
            cmd.append('--dry-run')
        proc = subprocess.Popen(cmd, shell=False)
        proc.communicate()
        return
