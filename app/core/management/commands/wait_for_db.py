import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management import BaseCommand



class Command(BaseCommand):
    """Django command to pause execution until db is available."""
    
    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database is unavailable, Waiting 1 second...')
                time.sleep('1')
            
        self.stdout.write(self.style.SUCCESS('Database is available now!'))


"""
    actually with mocking we did something. it will wait for 1 second like it works but we remove that one second :) 
    it is for trial in production we shouldn't make that 1 second sleeps!
"""