from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from contact.models import ContactMessage


@receiver(post_save, sender=ContactMessage)
def notify_admin_contact(sender, instance, created, **kwargs):

    if created:

        send_mail(
            subject=f"New Contact Message - {instance.subject}",
            message=instance.message,
            from_email="noreply@staging.dominioncitadelschools.com",
            recipient_list=["info@dominioncitadelschools.com"],
        )