from django.db.models.signals import post_save
from django.dispatch import receiver
from academics.models.co_curriculum import Activity
from academics.models.acadmic_year import AcademicYear


@receiver(post_save, sender=Activity)
def activity_created_logger(sender, instance, created, **kwargs):

    if created:
        print(f"New activity created: {instance.name}")


@receiver(post_save, sender=AcademicYear)
def ensure_single_active_year(sender, instance, created, **kwargs):

    if instance.is_active:

        AcademicYear.objects.exclude(id=instance.id).update(
            is_active=False
        )