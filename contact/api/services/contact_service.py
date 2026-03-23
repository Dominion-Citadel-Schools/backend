from contact.models import ContactMessage


class ContactService:

    @staticmethod
    def create_contact(data):

        contact = ContactMessage.objects.create(**data)

        return contact


    @staticmethod
    def mark_resolved(contact):

        contact.is_resolved = True
        contact.save(update_fields=["is_resolved"])

        return contact