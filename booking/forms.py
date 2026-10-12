from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Appointment


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class BookingForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["reason"]
        labels = {"reason": "Reason for visit"}
        widgets = {
            "reason": forms.Textarea(attrs={"rows": 3, "maxlength": 300}),
        }

    def clean_reason(self):
        reason = self.cleaned_data["reason"].strip()
        if len(reason) < 5:
            raise forms.ValidationError("Please describe the reason in at least 5 characters.")
        return reason
