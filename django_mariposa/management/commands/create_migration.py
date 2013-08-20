import subprocess
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = 'first arg is the name of the migration'
    help = 'create a migration file in MARIPOSA_DIRECTORY'
    option_list = BaseCommand.option_list + (
        make_option('-n', '--dry-run',
                    action='store_true',
                    dest='dry-run',
                    default=False,
                    help='dry-run',
        ),
        make_option('-t', '--type',
                    dest='type',
                    default='sql',
                    help='extension of script, either sql or py/rb/pl',
        ),
    )

    def handle(self, *args, **options):
        # d for MARIPOSA_DIRECTORY
        d = getattr(settings, "MARIPOSA_DIRECTORY")
        if not d:
            raise CommandError('settings must specify MARIPOSA_DIRECTORY')

        try:
            slug = args[0]
        except IndexError:
            raise CommandError('first positional argument is migration name')

        cmd = [
            "mariposa",
            "create",
            args[0],
            options['type'],
            "-d", '%s' % d,
        ]
        if options['dry-run']:
            cmd.append('--dry-run')
        proc = subprocess.Popen(cmd, shell=False)
        proc.communicate()
        return
