from django.core.management.base import BaseCommand
from django.db.utils import OperationalError

from psycopg2 import OperationalError as OperationalErrorg2

import time


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_up = False
        wait_count = 0
        while db_up is False and wait_count < 10:
            try:
                self.check(databases=['default'])
                db_up = True
            except(OperationalError, OperationalErrorg2):
                wait_count += 1
                self.stdout.write('Database unavailable. Waiting 1 second...')
                time.sleep(1)

        if wait_count == 10:
            self.stdout.write(self.style.ERROR('Failed to connect to database'))
        else:
            self.stdout.write(self.style.SUCCESS('Database available'))
