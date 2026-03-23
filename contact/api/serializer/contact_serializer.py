from rest_framework import serializers
from contact.models import ContactMessage
import requests
from decouple import config
from core.utils.text_filters import clean_text
from better_profanity import profanity


class ContactMessageSerializer(serializers.ModelSerializer):

    recaptcha_token = serializers.CharField(write_only=True)
    bot_field = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = ContactMessage
        fields = "__all__"
        read_only_fields = ["is_resolved", "created_at", "resolved_by", "resolved_at"]

    # field level validation
    def validate_full_name(self, value):

        if len(value) < 3:
            raise serializers.ValidationError(
                "Full name must contain at least 3 characters."
            )

        return value

    def validate_message(self, value):

        if len(value) < 10:
            raise serializers.ValidationError(
                "Message must be detailed enough."
            )

        if not value:
            return value

        if profanity.contains_profanity(value):
                raise serializers.ValidationError(
                    "Please remove inappropriate language."
            )

        return clean_text(value)

        

    # object level validation
    def validate(self, attrs):

        email = attrs.get("email")
        phone = attrs.get("phone_number")

        if not email and not phone:
            raise serializers.ValidationError(
                "Provide either email or phone number."
            )

        return attrs
    
    # Honeypot Field (Anti-bot trick)
    def validate_bot_field(self, value):
        if value:
            raise serializers.ValidationError("Bot detected.")
        return value

    
    # spam protection validation
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
    
   