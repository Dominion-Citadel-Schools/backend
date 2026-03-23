from django.core.management.base import BaseCommand
from core.seeders.registry import SEEDERS

# Import seeders so they register
import core.seeders.media.image_seeder
#import core.seeders.media.audio_seeder
import core.seeders.about.director_seeder
import core.seeders.about.history_seeder
import core.seeders.about.mission_seeder
import core.seeders.about.song_seeder
import core.seeders.about.vision_seeder
import core.seeders.academics.calender_seeder
import core.seeders.academics.cocurricular_seeder
import core.seeders.about.schooltour_seeder
import core.seeders.academics.campuse_seeder
import core.seeders.academics.program_seeder
import core.seeders.core.hero_section_seeder
import core.seeders.core.site_statistic_seeder
import core.seeders.core.why_choose_us_seeder
import core.seeders.testimonial.testimonial_seeder
import core.seeders.gallery.gallery_seeder




class Command(BaseCommand):

    help = "Run all database seeders"

    def handle(self, *args, **kwargs):

        self.stdout.write("Starting database seeding...\n")

        for seeder in SEEDERS:

            self.stdout.write(f"Running {seeder.__class__.__name__}...")
            seeder.seed()

        self.stdout.write(
            self.style.SUCCESS("\nDatabase seeding completed.")
        )