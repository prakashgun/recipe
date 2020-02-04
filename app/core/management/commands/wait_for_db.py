import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to pause execution until database is avaialable"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = None

        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Db connection not '
                                  'available, waiting for one second')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
