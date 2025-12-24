from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.urls import reverse_lazy
from .forms import RegisterForm
from core.models import Property
import qrcode
from io import BytesIO
from django.core.files import File

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create Property
            prop = Property.objects.create(
                owner=user,
                property_type=form.cleaned_data['property_type'],
                address=form.cleaned_data['address'],
                building_name=form.cleaned_data.get('building_name'),
                flat_no=form.cleaned_data.get('flat_no'),
            )
            # QR Generation
            qr_url = f'http://127.0.0.1:8000/visitor-entry/{prop.id}/'  # Change to your domain in production
            if prop.property_type == 'building' and prop.building_name:
                existing = Property.objects.filter(property_type='building', building_name=prop.building_name).exclude(id=prop.id).first()
                if existing and existing.qr_code:
                    prop.qr_code = existing.qr_code  # Share existing QR
                else:
                    qr = qrcode.QRCode()
                    qr.add_data(qr_url)
                    qr.make(fit=True)
                    img = qr.make_image(fill='black', back_color='white')
                    buffer = BytesIO()
                    img.save(buffer, format='PNG')
                    prop.qr_code.save(f'qr_building_{prop.building_name}.png', File(buffer))
            else:
                qr = qrcode.QRCode()
                qr.add_data(qr_url)
                qr.make(fit=True)
                img = qr.make_image(fill='black', back_color='white')
                buffer = BytesIO()
                img.save(buffer, format='PNG')
                prop.qr_code.save(f'qr_{prop.id}.png', File(buffer))
            prop.save()
            login(request, user)
            messages.success(request, 'Registration successful! Your QR is ready.')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')

# Use Django's built-in LoginView (no custom form needed)
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

# Password Reset Views
class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'