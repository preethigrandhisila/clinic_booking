from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Doctor(models.Model):
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="doctors")
    name = models.CharField(max_length=120)
    specialization = models.CharField(max_length=120)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"Dr. {self.name}"


class TimeSlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="slots")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ["date", "start_time"]
        constraints = [
            models.UniqueConstraint(fields=["doctor", "date", "start_time"], name="unique_doctor_slot"),
        ]

    def clean(self):
        if self.end_time and self.start_time and self.end_time <= self.start_time:
            raise ValidationError("The end time must be after the start time.")

    @property
    def is_booked(self):
        return hasattr(self, "appointment")

    def __str__(self):
        return f"{self.doctor} on {self.date:%d %b %Y} at {self.start_time:%H:%M}"


class Appointment(models.Model):
    """One appointment per slot. Cancelling deletes the row, which frees the slot."""

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="appointments")
    slot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE, related_name="appointment")
    reason = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["slot__date", "slot__start_time"]

    def __str__(self):
        return f"{self.patient.username}: {self.slot}"
