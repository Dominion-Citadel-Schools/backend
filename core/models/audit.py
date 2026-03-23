from django.db import models
from django.conf import settings


class AuditFields(models.Model):
    created_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="%(class)s_created"
    )

    updated_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="%(class)s_updated"
    )

    deleted_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="%(class)s_deleted"
    )

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    

    @property
    def created_name(self):
        if self.created_by:
            name = self.created_by.get_full_name()
            if name:
                return name
            return self.created_by.username
        return "-"
    
    @property
    def updated_name(self):
        if self.updated_by:
            name = self.updated_by.get_full_name()
            if name:
                return name
            return self.updated_by.username
        return "-"
    
    @property
    def deleted_name(self):
        if self.deleted_by:
            name = self.deleted_by.get_full_name()
            if name:
                return name
            return self.deleted_by.username
        return "-"
    