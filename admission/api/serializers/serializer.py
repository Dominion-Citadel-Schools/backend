from rest_framework import serializers
from admission.models.child_model import Admission, Child
from admission.models.admission_form_builder import AdmissionForm, AdmissionFormField
from admission.models.admisssion_document import AdmissionDocument
from better_profanity import profanity
from core.utils.text_filters import clean_text



class ChildSerializer(serializers.ModelSerializer):

    class Meta:
        model = Child
        exclude = ["admission"]

    def validate_age(self, value):

        if value < 2:
            raise serializers.ValidationError("Child too young for admission")

        return value
    

class AdmissionDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdmissionDocument
        fields = [
            "id",
            "document_type",
            "file",
            "uploaded_at",
        ]
        exclude = ["admission"]

    def validate_file(self, file):

        allowed = ["pdf", "jpg", "jpeg", "png"]

        ext = file.name.split(".")[-1].lower()

        if ext not in allowed:
            raise serializers.ValidationError(
                "Unsupported file format"
            )

        return file


class AdmissionSerializer(serializers.ModelSerializer):

    children = ChildSerializer(many=True)
    documents = AdmissionDocumentSerializer(many=True, required=False)

    class Meta:
        model = Admission
        fields = "__all__"

    def validate_additional_information(self, value):
        if not value:
            return value

        if profanity.contains_profanity(value):
            raise serializers.ValidationError(
                "Please remove inappropriate language."
            )

        return clean_text(value)

    def validate(self, data):

        children = data.get("children", [])
        declared_children = data.get("number_of_children")

        if len(children) != declared_children:
            raise serializers.ValidationError(
                f"Expected {declared_children} children but got {len(children)}."
            )

        return data

    def create(self, validated_data):

        children_data = validated_data.pop("children")
        documents_data = validated_data.pop("documents", [])

        admission = Admission.objects.create(**validated_data)

        for child in children_data:
            Child.objects.create(admission=admission, **child)

        # Only create documents if provided
        for doc in documents_data:
            AdmissionDocument.objects.create(admission=admission, **doc)

        return admission


class AdmissionFormFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdmissionFormField
        fields = [
            "id",
            "label",
            "field_type",
            "required",
            "options",
        ]


class AdmissionFormSerializer(serializers.ModelSerializer):

    fields = AdmissionFormFieldSerializer(many=True)

    class Meta:
        model = AdmissionForm
        fields = [
            "id",
            "name",
            "fields",
        ]



