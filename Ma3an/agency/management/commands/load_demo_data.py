from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from django.core.files import File
from django.conf import settings
import os
import random
from datetime import date, timedelta, time

from accounts.models import (
    Traveler, Agency, TourGuide, Language, Notification
)
from agency.models import (
    Subscription, Tour, TourSchedule, Geofence,
    GeofenceEvent, AgencySubscription
)
from traveler.models import (
    TravelerLocation, Review
)

User = get_user_model()


class Command(BaseCommand):
    help = "Load realistic demo data for Ma3an project"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("⏳ Loading demo data..."))

        # =========================
        # 1. Languages
        # =========================
        languages = [
            ("ar", "Arabic"),
            ("en", "English"),
            ("fr", "French"),
            ("es", "Spanish"),
        ]

        language_objs = []
        for code, name in languages:
            obj, _ = Language.objects.get_or_create(code=code, name=name)
            language_objs.append(obj)

        # =========================
        # 2. Subscriptions
        # =========================
        basic = Subscription.objects.get(subscriptionType="basic")
        standard = Subscription.objects.get(subscriptionType="standard")
        premium = Subscription.objects.get(subscriptionType="premium")

        # =========================
        # 3. Agencies + Users
        # =========================
        agencies = []
        for i in range(1, 4):
            user = User.objects.create_user(
                username=f"agency{i}",
                email=f"agency{i}@maan.sa",
                password="12345678",
                role="agency",
                first_name="Agency",
                last_name=str(i),
            )

            agency = Agency.objects.create(
                user=user,
                agency_name=f"Desert Explore {i}",
                phone_number=f"+966500000{i}",
                city=random.choice(["Riyadh", "Jeddah", "AlUla"]),
                approval_status="approved",
            )

            AgencySubscription.objects.create(
                agency=agency,
                plan=random.choice([basic, standard, premium]),
                start_date=date.today(),
                expiry_date=date.today() + timedelta(days=365),
            )

            agencies.append(agency)

        # =========================
        # 4. Tour Guides
        # =========================
        tour_guides = []
        for i in range(1, 6):
            user = User.objects.create_user(
                username=f"guide{i}",
                email=f"guide{i}@maan.sa",
                password="12345678",
                role="tourGuide",
                first_name="Guide",
                last_name=str(i),
            )

            guide = TourGuide.objects.create(
                user=user,
                agency=random.choice(agencies),
                phone=f"+966511111{i}",
                nationality="SA",
                is_active=True,
            )
            guide.languages.set(random.sample(language_objs, 2))
            tour_guides.append(guide)

        # =========================
        # 5. Travelers
        # =========================
        travelers = []
        for i in range(1, 11):
            user = User.objects.create_user(
                username=f"traveler{i}",
                email=f"traveler{i}@maan.sa",
                password="12345678",
                role="traveler",
                first_name="Traveler",
                last_name=str(i),
            )

            traveler = Traveler.objects.create(
                user=user,
                phone_number=f"+966522222{i}",
                nationality="SA",
                passport_number=f"P{i}234567",
            )
            travelers.append(traveler)

        # =========================
        # 6. Tours
        # =========================
        image_dir = os.path.join(settings.MEDIA_ROOT, "demo")
        image_files = os.listdir(image_dir)

        tours = []
        for i in range(1, 6):
            tour = Tour.objects.create(
                name=f"AlUla Adventure {i}",
                description="Explore heritage sites, nature and culture.",
                country="Saudi Arabia",
                city="AlUla",
                travelers=20,
                price=Decimal("1500.00"),
                start_date=date.today() + timedelta(days=10),
                end_date=date.today() + timedelta(days=15),
                days=5,
                agency=random.choice(agencies),
                tour_guide=random.choice(tour_guides),
            )

            # attach image
            image_path = os.path.join(image_dir, image_files[i % len(image_files)])
            with open(image_path, "rb") as img:
                tour.image.save(
                    image_files[i % len(image_files)],
                    File(img),
                    save=True
                )

            tours.append(tour)


        # =========================
        # 7. Schedules + Geofences
        # =========================
        schedules = []
        for tour in tours:
            for day in range(1, 4):
                schedule = TourSchedule.objects.create(
                    tour=tour,
                    day_number=day,
                    start_time=time(9, 0),
                    end_time=time(13, 0),
                    activity_title=f"Activity Day {day}",
                    description="Guided tour and free exploration.",
                    location_name="AlUla Old Town",
                    latitude=26.6084,
                    longitude=37.9232,
                )
                schedules.append(schedule)

                Geofence.objects.create(
                    schedule=schedule,
                    radius_meters=200,
                    trigger_on_enter=True,
                    trigger_on_exit=True,
                )

        # =========================
        # 8. Geofence Events + Notifications
        # =========================
        for traveler in travelers:
            schedule = random.choice(schedules)
            geofence = schedule.geofence
            guide = schedule.tour.tour_guide

            event = GeofenceEvent.objects.create(
                traveler=traveler,
                tour_guide=guide,
                geofence=geofence,
                event_type="exit",
            )

            Notification.objects.create(
                user=traveler.user,
                event=event,
                message="You left the activity area. Please return.",
            )

        # =========================
        # 9. Traveler Locations
        # =========================
        for traveler in travelers:
            TravelerLocation.objects.create(
                traveler=traveler,
                tour=random.choice(tours),
                latitude=26.60 + random.random() / 100,
                longitude=37.92 + random.random() / 100,
                accuracy=5.0,
            )

        # =========================
        # 10. Reviews
        # =========================
        for traveler in travelers:
            Review.objects.create(
                traveler=traveler,
                tour=random.choice(tours),
                rating=random.randint(3, 5),
                comment="Amazing experience, very well organized!",
            )

        self.stdout.write(self.style.SUCCESS("✅ Demo data loaded successfully!"))
