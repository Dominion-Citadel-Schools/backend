from core.models.sitestatistic import SiteStatistic
from core.seeders.base_seeder import BaseSeeder
from core.seeders.registry import register


class SiteStatisticSeeder(BaseSeeder):

    dataset_file = "core/site_statistic.yaml"

    def seed(self):
        data = self.load_dataset()

        for item in data.get("SiteStatistic", []):

            SiteStatistic.objects.update_or_create(
                label=item["label"],
                defaults={
                    "value": item["value"],
                    "icon": item["icon"],
                    "is_active": item.get("is_active", True),
                }
            )


register(SiteStatisticSeeder)