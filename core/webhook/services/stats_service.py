from pydoc import html
from urllib import response

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.db import transaction
from core.webhook.models.school_dasboard_stat import SchoolStats, CampusStats


class StatsService:

    BASE_URL = "https://dcs.eschoolng.net"
    LOGIN_URL = f"{BASE_URL}/admin/login.php"
    DASHBOARD_URL = f"{BASE_URL}/admin/?w=dashboard"

    @classmethod
    def login(cls):
        session = requests.Session()

        # Step 1: get login page (sets cookies)
        session.get(cls.LOGIN_URL)

        payload = {
            "username": settings.THIRD_PARTY_USERNAME,
            "password": settings.THIRD_PARTY_PASSWORD,
            "submit": "Login",
        }

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": cls.LOGIN_URL,
            "Origin": cls.BASE_URL,
        }

        response = session.post(cls.LOGIN_URL, data=payload, headers=headers)

        print("LOGIN STATUS:", response.status_code)
        print("COOKIES:", session.cookies.get_dict())
        print("URL:", response.url)

        if "login" in response.url.lower():
            raise Exception("Login failed")

        return session

    @classmethod
    def parse_dashboard(cls, html):
        soup = BeautifulSoup(html, "html.parser")

        stats = soup.select("div.smallstat.box")

        total_students = 0
        total_staff = 0
        campuses = []

        for stat in stats:
            title_tag = stat.select_one(".title")
            value_tag = stat.select_one(".value")

            if not title_tag or not value_tag:
                continue

            title = title_tag.text.strip()
            value_text = value_tag.text.strip()

            # Clean value
            try:
                value = int(value_text)
            except:
                continue

            # 🔹 GLOBAL STATS
            if title == "Students":
                # Check if it's total or campus
                more_text = stat.select_one(".more span")

                if more_text:
                    label = more_text.text.strip()

                    if "Total No. of Student" in label:
                        total_students = value
                    else:
                        # This is a campus
                        campus_name = label.strip().upper()
                        campuses.append({
                            "name": campus_name,
                            "students": value
                        })

            elif title == "Staff":
                total_staff = value

        return {
            "total_students": total_students,
            "total_staff": total_staff,
            "campuses": campuses
        }

    @classmethod
    @transaction.atomic
    def save(cls, data):
        SchoolStats.objects.update_or_create(
            id=1,
            defaults={
                "total_students": data["total_students"],
                "total_staff": data["total_staff"]
            }
        )

        for campus in data["campuses"]:
            CampusStats.objects.update_or_create(
                campus_name=campus["name"],
                defaults={
                    "total_students": campus["students"]
                }
            )

    @classmethod
    def run_sync(cls):
        print("🔐 Logging in...")
        session = cls.login()

        print("📡 Fetching dashboard...")
        response = session.get(
            cls.DASHBOARD_URL,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Referer": cls.LOGIN_URL,
            }
        )

        print("STATUS:", response.status_code)
        print("URL:", response.url)
        print("PREVIEW:", response.text[:300])

        if response.status_code != 200:
            raise Exception("Failed to fetch dashboard")

        if "login" in response.url.lower():
            raise Exception("Not authenticated")

        if "Students" not in response.text:
            raise Exception("Dashboard content missing")

        print("Parsing data...")
        data = cls.parse_dashboard(response.text)

        print("Saving to database...")
        cls.save(data)

        print("Sync complete")

        return data