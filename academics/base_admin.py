from django.contrib import admin


class BaseValidatedAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)
