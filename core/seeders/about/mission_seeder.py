from about.models.mission import Mission, CoreValue
from core.seeders.base_seeder import BaseSeeder
from core.seeders.registry import register


class MissionSeeder(BaseSeeder):

    dataset_file = "about/mission.yaml"

    def seed(self):

        data = self.load_dataset()["mission_section"]

        mission = Mission.objects.update_or_create(
            section_type=data["section_type"],
            defaults={
                "statement": data["statement"],
                "is_active": data["is_active"],
            }
        )[0]

        mission.core_values.all().delete()

        for value in data["core_values"]:
            CoreValue.objects.create(
                mission=mission,
                title=value["title"],
                description=value["description"],
            )


register(MissionSeeder)