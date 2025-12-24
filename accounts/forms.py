from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True)
    phone = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    property_type = forms.ChoiceField(
        choices=[('bungalow', 'Bungalow/Independent'), ('building', 'Apartment Building')],
        required=True
    )
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    building_name = forms.CharField(max_length=255, required=False)
    flat_no = forms.CharField(max_length=50, required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'full_name', 'phone', 'password1', 'password2')