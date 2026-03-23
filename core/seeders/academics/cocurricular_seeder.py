from academics.models.co_curriculum import ActivityCategory, Activity
from core.seeders.base_seeder import BaseSeeder
from core.seeders.registry import register


class CocurricularSeeder(BaseSeeder):

    dataset_file = "academics/cocurricular.yaml"

    def seed(self):

        data = self.load_dataset()

        for category_data in data["categories"]:

            category, _ = ActivityCategory.objects.get_or_create(
                name=category_data["name"],
                defaults={
                    "icon": category_data.get("icon"),
                    "order": category_data.get("order", 0),
                    "is_active": True
                }
            )

            for index, activity_name in enumerate(category_data["activities"], start=1):

                Activity.objects.get_or_create(
                    category=category,
                    name=activity_name,
                    defaults={
                        "status": "ACTIVE",
                        "order": index
                    }
                )



register(CocurricularSeeder)