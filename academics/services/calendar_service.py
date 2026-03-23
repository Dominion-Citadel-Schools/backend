from academics.models.acadmic_year import AcademicYear
from collections import defaultdict


class CalendarService:

    @staticmethod
    def get_active_calendar():

        return (
            AcademicYear.objects
            .filter(is_active=True)
            .prefetch_related("events")
            .first()
        )

    @staticmethod
    def get_current_calendar():

        academic_year = (
            AcademicYear.objects
            .filter(is_active=True)
            .prefetch_related("events")
            .first()
        )

        if not academic_year:
            return None

        months = defaultdict(list)
        holidays = []
        exams = []

        for event in academic_year.events.all():

            event_data = {
                "title": event.title,
                "date": event.date,
                "color": event.color_code
            }

            if event.event_type == "EVENT":
                months[event.month].append(event_data)

            elif event.event_type == "HOLIDAY":
                holidays.append(event_data)

            elif event.event_type == "EXAM":
                exams.append(event_data)

        return {
            "academic_year": academic_year.name,
            "download_calendar": academic_year.calendar_file.url if academic_year.calendar_file else None,
            "months": months,
            "holidays": holidays,
            "exam_periods": exams
        }

    @staticmethod
    def get_calendar_events(academic_year):

        return academic_year.events.all()