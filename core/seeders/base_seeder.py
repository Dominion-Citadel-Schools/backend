from django.conf import settings
import os
import yaml
import json


class BaseSeeder:

    dataset_file = None

    def get_environment(self):

        env = getattr(settings, "APP_ENV", "dev")
        
        return env.lower()

    def get_dataset_path(self):

        env = self.get_environment()

        return os.path.join(
            settings.BASE_DIR,
            "core",
            "datasets",
            env,
            self.dataset_file
        )

    def load_dataset(self):

        path = self.get_dataset_path()

        if path.endswith(".yaml") or path.endswith(".yml"):
            with open(path) as f:
                return yaml.safe_load(f)

        if path.endswith(".json"):
            with open(path) as f:
                return json.load(f)

        raise Exception("Unsupported dataset format")

    def seed(self):
        raise NotImplementedError