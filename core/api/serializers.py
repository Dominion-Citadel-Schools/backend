from rest_framework import serializers
from ..models.whychooseusitem import WhyChooseUsItem
from ..models.sitestatistic import SiteStatistic
from ..models.herosection import HeroSection


class HeroSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSection
        fields = "__all__"
        read_only_fields = ("updated_at",)

    def validate_headline(self, value):
        value = value.strip()
        if len(value) < 5:
            raise serializers.ValidationError("Headline too short.")
        return value

    def validate(self, attrs):
        secondary_text = attrs.get("secondary_cta_text")
        secondary_url = attrs.get("secondary_cta_url")

        if secondary_text and not secondary_url:
            raise serializers.ValidationError(
                {"secondary_cta_url": "Secondary CTA URL required."}
            )

        if secondary_url and not secondary_text:
            raise serializers.ValidationError(
                {"secondary_cta_text": "Secondary CTA text required."}
            )

        return attrs


class SiteStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteStatistic
        fields = ["label", "value", "icon"]


class WhyChooseUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyChooseUsItem
        fields = ["title", "description", "icon"]


'''class MediaSerializer(serializers.ModelSerializer):
    file_size = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = "__all__"
        read_only_fields = ("uploaded_at",)

    def get_file_size(self, obj):
        if obj.file:
            return obj.file.size
        return None

    def get_file_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.file.url)'''
