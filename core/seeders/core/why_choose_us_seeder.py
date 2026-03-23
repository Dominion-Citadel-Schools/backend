from core.models.whychooseusitem import WhyChooseUsItem
from core.seeders.base_seeder import BaseSeeder
from core.seeders.registry import register


class WhyChooseUsSeeder(BaseSeeder):

    dataset_file = "core/why_choose_us.yaml"

    def seed(self):
        data = self.load_dataset()

        for item in data.get("WhyChooseUsItem", []):

            WhyChooseUsItem.objects.update_or_create(
                title=item["title"],
                defaults={
                    "description": item["description"],
                    "icon": item["icon"],
                    "is_active": item.get("is_active", True),
                }
            )


register(WhyChooseUsSeeder)