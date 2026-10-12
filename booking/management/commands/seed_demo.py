from datetime import time, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from booking.models import Department, Doctor, TimeSlot

DEMO = {
    "Cardiology": [("Anita Rao", "Interventional cardiology", 800)],
    "General Medicine": [("Suresh Kumar", "Internal medicine", 500), ("Meera Nair", "Family medicine", 500)],
    "Dermatology": [("Priya Sharma", "Cosmetic and clinical dermatology", 700)],
}
SLOT_HOURS = (9, 10, 11, 14, 15, 16)


class Command(BaseCommand):
    help = "Load demo departments, doctors and time slots for the next 7 days."

    def handle(self, *args, **options):
        today = timezone.localdate()
        for dept_name, doctors in DEMO.items():
            dept, _ = Department.objects.get_or_create(
                name=dept_name, defaults={"description": f"{dept_name} services."}
            )
            for name, spec, fee in doctors:
                doctor, _ = Doctor.objects.get_or_create(
                    name=name,
                    defaults={"department": dept, "specialization": spec, "consultation_fee": fee},
                )
                for offset in range(1, 8):
                    day = today + timedelta(days=offset)
                    for hour in SLOT_HOURS:
                        TimeSlot.objects.get_or_create(
                            doctor=doctor, date=day, start_time=time(hour),
                            defaults={"end_time": time(hour, 30)},
                        )
        self.stdout.write(self.style.SUCCESS("Demo data loaded."))
