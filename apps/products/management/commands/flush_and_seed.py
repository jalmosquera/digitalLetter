from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Flush DB (non-interactive), migrate and seed demo data."

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("Flushing database..."))
        call_command('flush', '--no-input')

        self.stdout.write(self.style.MIGRATE_HEADING("Applying migrations..."))
        call_command('migrate', '--no-input')

        self.stdout.write(self.style.MIGRATE_HEADING("Seeding demo data..."))
        call_command('seed_demo')

        self.stdout.write(self.style.SUCCESS("Database flushed and demo data seeded."))





