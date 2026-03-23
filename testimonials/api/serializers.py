from decouple import config
import requests
from rest_framework import serializers
from django.utils import timezone
from ..models import Testimonial


class TestimonialSerializer(serializers.ModelSerializer):
    
    recaptcha_token = serializers.CharField(write_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Testimonial
        fields = [
            "full_name",
            "role",
            "rating",
            "rating",
            "message",
            "class_level",
            "graduation_year",
            "recaptcha_token",
            "status",
            "image_id",
            "image_url",
        ]
        

    def get_image_url(self, obj):
        if obj.image and obj.image.file:
            request = self.context.get("request")
            url = obj.image.file.url
            return request.build_absolute_uri(url) if request else url
        return None

    def validate(self, attrs):
        token = attrs.pop("recaptcha_token")

        response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": config("RECAPTCHA_SECRET_KEY"),
                "response": token
            }
        )

        result = response.json()

        if not result.get("success") or result.get("score", 0) < 0.5:
         raise serializers.ValidationError("Invalid reCAPTCHA.")

        return attrs

    def validate_full_name(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError(
                "Full name must be at least 3 characters."
            )
        return value

    def validate_message(self, value):
        value = value.strip()
        if len(value) < 10:
            raise serializers.ValidationError(
                "Message is too short."
            )
        return value

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )
        return value

    def validate(self, attrs):
        role = attrs.get("role")
        graduation_year = attrs.get("graduation_year")
        class_level = attrs.get("class_level")

        current_year = timezone.now().year

        if role == "ALUMNI":
            if not graduation_year:
                raise serializers.ValidationError({
                    "graduation_year": "Graduation year required for alumni."
                })
            if graduation_year > current_year:
                raise serializers.ValidationError({
                    "graduation_year": "Cannot be in the future."
                })

        if role != "ALUMNI" and graduation_year:
            raise serializers.ValidationError({
                "graduation_year": "Only alumni can have graduation year."
            })
        
        if role == "STUDENT":
            if not class_level:
                raise serializers.ValidationError({
                    "class_level": "class_level required for students."
                })
            if class_level > 40:
                raise serializers.ValidationError({
                    "class_level": "Cannot exceed 40 characters."
                })

        if role != "STUDENT" and class_level:
            raise serializers.ValidationError({
                "class_level": "Only students can have class_level."
            })

        return attrs
