from django.core.management.base import BaseCommand, CommandError
from shortener.models import ShortURL

class Command(BaseCommand):
    help = 'Refrehes all ShortURL shortcode'

    def add_arguments(self, parser):
        parser.add_argument('--items', type=int)  # python manage.py refreshcodes --items n

    def handle(self, *args, **options):
        return ShortURL.objects.refresh_shortcodes(items=options['items'])