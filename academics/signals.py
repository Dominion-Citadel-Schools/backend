from django.db.models.signals import post_save
from django.dispatch import receiver
from academics.models.acadmic_year import AcademicYear



@receiver(post_save, sender=AcademicYear)
def ensure_single_active_year(sender, instance, created, **kwargs):

    if instance.is_active:

        AcademicYear.objects.exclude(id=instance.id).update(
            is_active=False
        )