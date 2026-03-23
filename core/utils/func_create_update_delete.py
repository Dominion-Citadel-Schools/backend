from django.utils.timezone import now

def set_created_by(obj, user):
    """
    Set creator of the record.
    """
    if not obj.pk: # new object
        obj.created_by = user


def set_updated_by(obj, user):
    obj.updated_by = user


def set_deleted_by(obj, user):
    obj.deleted_by = user

def bulk_delete_with_audit(queryset, user):

    for obj in queryset:
        obj.deleted_by = user
        obj.deleted_at = now()
        obj.is_deleted = True
        obj.save()