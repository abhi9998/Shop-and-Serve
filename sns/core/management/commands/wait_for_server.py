import time
import requests
import os

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until Django server is available"""

    def handle(self, *args, **options):
        self.stdout.write("...Waiting for Django server...")
        conn = None
        hostname = "app:8000"
        while not conn:
            try:
                response = requests.get("http://app:8000/api/store/info")
                break
            except Exception:
                self.stdout.write('Django server is unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Django server is Available!'))
