from academics.models.co_curriculum import Activity, ActivityCategory


class ActivityService:

    @staticmethod
    def create_activity(data):
        return Activity.objects.create(**data)

    @staticmethod
    def update_activity(instance, data):

        for key, value in data.items():
            setattr(instance, key, value)

        instance.save()
        return instance

    @staticmethod
    def delete_activity(instance):
        instance.delete()

    @staticmethod
    def get_active_activities():

        return Activity.objects.filter(
            status="ACTIVE",
            category__is_active=True
        ).select_related("category")
    
    
    @staticmethod
    def get_co_curricular_activities():

        return (
            ActivityCategory.objects
            .filter(is_active=True)
            .prefetch_related("activities")
            .order_by("order")
        )