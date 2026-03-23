from django.db import transaction
from admission.models.admission_models import Admission
from admission.models.child_model import Child


class AdmissionService:

    @staticmethod
    @transaction.atomic
    def create_admission(validated_data):

        children_data = validated_data.pop("children")

        admission = Admission.objects.create(**validated_data)

        children = [
            Child(admission=admission, **child)
            for child in children_data
        ]

        Child.objects.bulk_create(children)

        return admission