from django.db import models


class SchoolStats(models.Model):
    total_students = models.PositiveIntegerField()
    total_staff = models.PositiveIntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Stats - Students: {self.total_students}, Staff: {self.total_staff}"


class CampusStats(models.Model):
    campus_name = models.CharField(max_length=255, unique=True)
    total_students = models.PositiveIntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.campus_name} - {self.total_students}"