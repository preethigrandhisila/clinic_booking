from django.contrib import admin

from .models import Appointment, Department, Doctor, TimeSlot


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("name", "specialization", "department", "consultation_fee", "is_active")
    list_filter = ("department", "is_active")
    search_fields = ("name", "specialization")


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ("doctor", "date", "start_time", "end_time")
    list_filter = ("doctor", "date")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "slot", "created_at")
    search_fields = ("patient__username", "reason")
