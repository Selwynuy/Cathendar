"""
Management command to populate holidays from the holidays library.
Usage: python manage.py populate_holidays --country US --year 2024
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
import holidays
from datetime import date, datetime
from core.models import Holiday


class Command(BaseCommand):
    help = 'Populate holidays from the holidays library for a given country and year'

    def add_arguments(self, parser):
        parser.add_argument(
            '--country',
            type=str,
            default='US',
            help='ISO country code (e.g., US, GB, CA, AU)',
        )
        parser.add_argument(
            '--year',
            type=int,
            default=None,
            help='Year to populate holidays for (defaults to current year)',
        )
        parser.add_argument(
            '--years',
            type=int,
            nargs=2,
            metavar=('START', 'END'),
            help='Range of years to populate (e.g., --years 2024 2025)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing holidays for the country before populating',
        )

    def handle(self, *args, **options):
        country = options['country'].upper()
        year = options['year']
        years_range = options['years']
        clear = options['clear']

        # Validate country code
        try:
            # Try to get holidays for the country to validate
            test_holidays = holidays.country_holidays(country, years=2024)
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Invalid country code: {country}. Error: {e}')
            )
            return

        # Determine years to process
        if years_range:
            start_year, end_year = years_range
            years = range(start_year, end_year + 1)
        elif year:
            years = [year]
        else:
            current_year = timezone.now().year
            years = [current_year, current_year + 1]  # Current and next year

        # Clear existing holidays if requested
        if clear:
            deleted_count = Holiday.objects.filter(country=country).delete()[0]
            self.stdout.write(
                self.style.WARNING(f'Deleted {deleted_count} existing holidays for {country}')
            )

        # Get holidays from the library
        country_holidays = holidays.country_holidays(country, years=years)

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for holiday_date, holiday_name in country_holidays.items():
            # Skip if date is in the past (optional - you might want to keep historical holidays)
            # if holiday_date < date.today():
            #     continue

            holiday, created = Holiday.objects.get_or_create(
                date=holiday_date,
                name=holiday_name,
                country=country,
                defaults={
                    'description': f'Public holiday in {country}',
                    'is_national': True,
                }
            )

            if created:
                created_count += 1
            else:
                # Update existing holiday if needed
                if holiday.description != f'Public holiday in {country}':
                    holiday.description = f'Public holiday in {country}'
                    holiday.save()
                    updated_count += 1
                else:
                    skipped_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated holidays for {country}:\n'
                f'  Created: {created_count}\n'
                f'  Updated: {updated_count}\n'
                f'  Skipped: {skipped_count}\n'
                f'  Total: {len(country_holidays)} holidays processed'
            )
        )

