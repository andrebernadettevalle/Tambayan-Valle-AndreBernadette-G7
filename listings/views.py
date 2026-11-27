from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Listing
from .forms import ListingForm


@login_required
def listing_list(request):
    listings = Listing.objects.select_related('owner').all()
    return render(request, 'listings/listing_list.html', {'listings': listings})


@login_required
def my_listings(request):
    listings = Listing.objects.filter(owner=request.user)
    return render(request, 'listings/my_listings.html', {'listings': listings})


@login_required
def listing_detail(request, pk):
    listing = get_object_or_404(Listing.objects.select_related('owner'), pk=pk)
    return render(request, 'listings/listing_detail.html', {'listing': listing})


@login_required
def listing_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, user=request.user)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            messages.success(request, "Your listing has been posted!")
            return redirect('listing-detail', pk=listing.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ListingForm(user=request.user)
    return render(request, 'listings/listing_form.html', {'form': form, 'action': 'Post New Listing'})


@login_required
def listing_update(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if listing.owner != request.user:
        messages.error(request, "You can only edit your own listings.")
        return redirect('listing-detail', pk=listing.pk)

    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Listing updated successfully.")
            return redirect('listing-detail', pk=listing.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ListingForm(instance=listing, user=request.user)
    return render(request, 'listings/listing_form.html', {'form': form, 'action': 'Edit Listing', 'listing': listing})


@login_required
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if listing.owner != request.user and request.user.role != 'admin':
        messages.error(request, "You do not have permission to delete this listing.")
        return redirect('listing-detail', pk=listing.pk)

    if request.method == 'POST':
        listing.delete()
        messages.success(request, "Listing deleted.")
        return redirect('listing-list')
    return render(request, 'listings/listing_confirm_delete.html', {'listing': listing})