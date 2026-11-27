from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from listings.models import Listing
from .forms import CustomUserCreationForm, ProfileUpdateForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.get_redirect_url()
        if next_url:
            return next_url
        if getattr(self.request.user, 'role', None) == 'admin':
            return reverse_lazy('admin-dashboard')
        return reverse_lazy('resident-dashboard')


def register(request):
    if request.user.is_authenticated:
        if getattr(request.user, 'role', None) == 'admin':
            return redirect('admin-dashboard')
        return redirect('resident-dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to TAMBAYAN! Your account has been created.")
            if getattr(user, 'role', None) == 'admin':
                return redirect('admin-dashboard')
            return redirect('resident-dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


register_view = register


@login_required
def admin_dashboard(request):
    if getattr(request.user, 'role', None) != 'admin':
        return redirect('resident-dashboard')
    recent_listings = Listing.objects.select_related('owner').all()[:10]
    context = {
        'user': request.user,
        'recent_listings': recent_listings,
        'total_listings': Listing.objects.count(),
        'open_listings': Listing.objects.filter(status='open').count(),
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
def resident_dashboard(request):
    if getattr(request.user, 'role', None) != 'resident':
        return redirect('admin-dashboard')
    user_listings = Listing.objects.filter(owner=request.user)[:5]
    context = {
        'user': request.user,
        'user_listings': user_listings,
        'my_open_count': Listing.objects.filter(owner=request.user, status='open').count(),
        'community_open_count': Listing.objects.filter(status='open').count(),
    }
    return render(request, 'accounts/resident_dashboard.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


profile_view = profile