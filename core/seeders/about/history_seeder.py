from about.models.history import HistorySection, AchievementStats
from media_config.models.image import Image
from core.seeders.base_seeder import BaseSeeder
from core.seeders.registry import register


class HistorySeeder(BaseSeeder):

    dataset_file = "about/history.yaml"

    def seed(self):

        data = self.load_dataset()
        history_data = data["history_section"]

        image = None
        if history_data.get("image"):
            image = Image.objects.filter(
                file=history_data["image"]
            ).first()

        HistorySection.objects.update_or_create(
            section_type="history",
            defaults={
                "title": history_data["title"],
                "content": history_data["content"],
                "founded_year": history_data["founded_year"],
                "image": image,
                "is_active": history_data["is_active"],
            }
        )

        stats = data["achievement_stats"]

        AchievementStats.objects.update_or_create(
            is_active=True,
            defaults={
                "years_of_excellence": stats["years_of_excellence"],
                "graduates": stats["graduates"],
                "faculty_members": stats["faculty_members"],
                "college_acceptance_rate": stats["college_acceptance_rate"],
            }
        )


register(HistorySeeder)