from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.doctor_list, name="doctor_list"),
    path("doctors/<int:pk>/", views.doctor_detail, name="doctor_detail"),
    path("api/doctors/<int:pk>/slots/", views.slots_api, name="slots_api"),
    path("slots/<int:slot_id>/book/", views.book_slot, name="book_slot"),
    path("appointments/", views.my_appointments, name="my_appointments"),
    path("appointments/<int:pk>/cancel/", views.cancel_appointment, name="cancel_appointment"),
    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(
        template_name="booking/auth.html",
        extra_context={"title": "Log in"},
    ), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
