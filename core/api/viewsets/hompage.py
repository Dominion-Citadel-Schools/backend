from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from core.models.herosection import HeroSection
from core.models.sitestatistic import SiteStatistic
from core.models.whychooseusitem import WhyChooseUsItem
from core.api.serializers import (
    HeroSectionSerializer,
    SiteStatisticSerializer,
    WhyChooseUsSerializer,
)







class HomePageViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        cached_data = cache.get("homepage_data")

        if cached_data:
            return Response(cached_data)

        hero = HeroSection.objects.filter(is_active=True).first()
        stats = SiteStatistic.objects.filter(is_active=True)
        why_choose_us = WhyChooseUsItem.objects.filter(is_active=True)

        data = {
            "hero": HeroSectionSerializer(hero).data if hero else None,
            "statistics": SiteStatisticSerializer(stats, many=True).data,
            "why_choose_us": WhyChooseUsSerializer(why_choose_us, many=True).data
        }

        cache.set("homepage_data", data, timeout=60 * 30)

        return Response(data)

