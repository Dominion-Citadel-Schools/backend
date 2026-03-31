from academics.models.program import Program, ProgramCampus
from media_config.models.image import Image
from core.seeders.base_seeder import BaseSeeder
from core.seeders.registry import register


class ProgramSeeder(BaseSeeder):

    dataset_file = "academics/program.yaml"

    def seed(self):
        data = self.load_dataset()

        for item in data.get("Program", []):

            # ✅ Resolve image safely
            image = None
            image_path = item.get("image")

            if image_path:
                image = Image.objects.filter(file=image_path).first()

                if not image:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Image not found for {item['title']}: {image_path}"
                        )
                    )

            #Create / update program
            program, _ = Program.objects.update_or_create(
                title=item["title"],
                defaults={
                    "category": item["category"],
                    "description": item["description"],
                    "full_day": item.get("full_day", True),
                    "is_active": item.get("is_active", True),
                    "image": image,
                }
            )

            #Reset campuses (idempotent seeding)
            ProgramCampus.objects.filter(program=program).delete()

            #Create campuses
            for idx, campus in enumerate(item.get("campuses", [])):
                ProgramCampus.objects.create(
                    program=program,
                    campus_name=campus["campus_name"],
                    features=campus.get("features", []),
                    order=idx
                )


register(ProgramSeeder)