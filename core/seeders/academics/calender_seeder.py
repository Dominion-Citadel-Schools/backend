from academics.models.acadmic_year import AcademicYear, CalendarEvent
from core.seeders.base_seeder import BaseSeeder
from core.seeders.registry import register


class CalenderSeeder(BaseSeeder):

    dataset_file = "academics/calendar.yaml"

    def seed(self):

        data = self.load_dataset()

        year_data = data["academic_year"]

        academic_year, _ = AcademicYear.objects.get_or_create(
            name=year_data["name"],
            defaults={
                "start_date": year_data["start_date"],
                "end_date": year_data["end_date"],
                "is_active": year_data["is_active"]
            }
        )

        for event in data["events"]:

            CalendarEvent.objects.get_or_create(
                academic_year=academic_year,
                title=event["title"],
                date=event["date"],
                defaults={
                    "month": event["month"],
                    "event_type": event["type"],
                    "color_code": event["color"]
                }
            )


register(CalenderSeeder)