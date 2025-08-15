import asyncio
from django.core.management.base import BaseCommand
from crawler.crawler import Crawler

class Command(BaseCommand):
    help = 'Crawls ebag.bg for product prices'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting crawler...'))

        crawler = Crawler()
        try:
            asyncio.run(crawler.run())
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Crawler failed: {e}'))
            return

        self.stdout.write(self.style.SUCCESS('Crawler finished successfully.'))
