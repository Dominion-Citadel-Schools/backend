from django.db import models
from django.core.exceptions import ValidationError


class AcademicYear(models.Model):

    name = models.CharField(max_length=100, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()

    calendar_file = models.FileField(
        upload_to="academic_calendars/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_date"]

    def clean(self):

        if self.start_date >= self.end_date:
            raise ValidationError(
                "End date must be greater than start date."
            )
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CalendarEvent(models.Model):

    EVENT_TYPE = (
        ("EVENT", "Event"),
        ("HOLIDAY", "Holiday"),
        ("EXAM", "Exam"),
    )

    academic_year = models.ForeignKey(
        AcademicYear,
        related_name="events",
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    date = models.DateField()

    month = models.CharField(max_length=20)

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPE
    )

    color_code = models.CharField(
        max_length=20,
        help_text="Used by frontend UI"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date"]
        indexes = [
        models.Index(fields=["date"]),
        ]

    def clean(self):

        if self.date < self.academic_year.start_date:
            raise ValidationError(
                "Event cannot be before academic year start."
            )

        if self.date > self.academic_year.end_date:
            raise ValidationError(
                "Event cannot be after academic year end."
            )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title