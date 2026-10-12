import datetime

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import BookingForm, SignUpForm
from .models import Appointment, Department, Doctor, TimeSlot


def parse_date(value):
    """Return the requested date, never earlier than today."""
    try:
        requested = datetime.date.fromisoformat(value)
    except (TypeError, ValueError):
        return timezone.localdate()
    return max(requested, timezone.localdate())


def open_slots(doctor, date):
    """Free slots for a doctor on a date, excluding times that have already passed."""
    qs = TimeSlot.objects.filter(doctor=doctor, date=date, appointment__isnull=True)
    if date == timezone.localdate():
        qs = qs.filter(start_time__gte=timezone.localtime().time())
    return qs


def doctor_list(request):
    doctors = Doctor.objects.filter(is_active=True).select_related("department")
    q = request.GET.get("q", "").strip()
    dept = request.GET.get("dept", "")
    if q:
        doctors = doctors.filter(Q(name__icontains=q) | Q(specialization__icontains=q))
    if dept.isdigit():
        doctors = doctors.filter(department_id=int(dept))
    return render(request, "booking/doctors.html", {
        "doctors": doctors,
        "departments": Department.objects.all(),
        "q": q,
        "dept": dept,
    })


def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor.objects.select_related("department"), pk=pk, is_active=True)
    date = parse_date(request.GET.get("date"))
    return render(request, "booking/doctor_detail.html", {
        "doctor": doctor,
        "date_str": date.isoformat(),
        "today": timezone.localdate().isoformat(),
        "slots": open_slots(doctor, date),
    })


def slots_api(request, pk):
    """JSON feed used by the date picker so slots update without a page reload."""
    doctor = get_object_or_404(Doctor, pk=pk, is_active=True)
    date = parse_date(request.GET.get("date"))
    slots = [
        {
            "label": f"{s.start_time:%H:%M} to {s.end_time:%H:%M}",
            "url": reverse("book_slot", args=[s.pk]),
        }
        for s in open_slots(doctor, date)
    ]
    return JsonResponse({"date": date.isoformat(), "slots": slots})


@login_required
def book_slot(request, slot_id):
    slot = get_object_or_404(TimeSlot.objects.select_related("doctor__department"), pk=slot_id)
    if not open_slots(slot.doctor, slot.date).filter(pk=slot.pk).exists():
        messages.error(request, "Sorry, that time is no longer available. Please choose another.")
        return redirect("doctor_detail", pk=slot.doctor_id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                # The OneToOne link from Appointment to TimeSlot is unique, so two
                # patients cannot both book the same slot, even at the same instant.
                with transaction.atomic():
                    appointment = form.save(commit=False)
                    appointment.patient = request.user
                    appointment.slot = slot
                    appointment.save()
            except IntegrityError:
                messages.error(request, "Someone just booked this time. Please pick another slot.")
                return redirect("doctor_detail", pk=slot.doctor_id)
            messages.success(
                request,
                f"Booked with {slot.doctor} on {slot.date:%d %b %Y} at {slot.start_time:%H:%M}.",
            )
            return redirect("my_appointments")
        messages.error(request, "Please fix the highlighted fields.")
    else:
        form = BookingForm()
    return render(request, "booking/book.html", {"form": form, "slot": slot})


@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user).select_related("slot__doctor")
    return render(request, "booking/my_appointments.html", {"appointments": appointments})


@login_required
@require_POST
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, patient=request.user)
    appointment.delete()
    messages.success(request, "Appointment cancelled. The time slot is open again.")
    return redirect("my_appointments")


def signup(request):
    if request.user.is_authenticated:
        return redirect("doctor_list")
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account is ready.")
        return redirect("doctor_list")
    return render(request, "booking/auth.html", {"form": form, "title": "Create account"})
