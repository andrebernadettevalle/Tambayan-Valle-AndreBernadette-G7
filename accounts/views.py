from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import CustomUserRegistrationForm, CustomUserProfileForm


def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        if self.request.user.role == 'admin':
            return '/accounts/admin-dashboard/'
        return '/accounts/resident-dashboard/'


@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('resident-dashboard')
    return render(request, 'accounts/admin_dashboard.html', {'user': request.user})


@login_required
def resident_dashboard(request):
    if request.user.role != 'resident':
        return redirect('admin-dashboard')
    return render(request, 'accounts/resident_dashboard.html', {'user': request.user})


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = CustomUserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form, 'user': request.user})