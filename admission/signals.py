from django.db.models.signals import post_save
from django.dispatch import receiver
from admission.models.admission_models import Admission
from django.core.mail import send_mail
from django.conf import settings



@receiver(post_save, sender=Admission)
def admission_created(sender, instance, created, **kwargs):

   if created:

        send_mail(
            subject="New Admission Application",
            message=f"""
            A new admission application was submitted.

        Parent Name: {instance.parent_name}
                Email: {instance.email}
        Phone: {instance.phone}
        Children: {instance.number_of_children}
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["info@dominioncitadelschools.com"],
            fail_silently=False,
        )

        send_mail(
            "Admission Application Received",
            "Thank you for applying. Our admissions team will contact you shortly.",
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
        )