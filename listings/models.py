from django.db import models
from django.conf import settings


class Listing(models.Model):
    LISTING_TYPE_CHOICES = [
        ('offer', 'Skill / Resource Offer'),
        ('need', 'Skill / Resource Need'),
    ]

    CATEGORY_CHOICES = [
        ('tutoring', 'Tutoring & Education'),
        ('repairs', 'Home & Electronics Repairs'),
        ('tools', 'Tools & Equipment Lending'),
        ('errands', 'Errands & Delivery'),
        ('household', 'Household & Gardening'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('fulfilled', 'Fulfilled'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listings'
    )
    title = models.CharField(max_length=150)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, default='offer')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField()
    location = models.CharField(max_length=120, help_text="e.g., Purok 3, Barangay Poblacion")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_listing_type_display()}] {self.title} by {self.owner.username}"