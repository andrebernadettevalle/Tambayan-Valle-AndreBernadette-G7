from django import forms
from .models import Listing


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('title', 'listing_type', 'category', 'description', 'location', 'status')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the skill, tool, or help needed...'}),
            'title': forms.TextInput(attrs={'placeholder': 'e.g., Math Tutoring or Power Drill Lending'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g., Purok 3, Barangay Poblacion'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Hide status field on initial creation; default is 'open'
        if not self.instance.pk:
            self.fields.pop('status')

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 4:
            raise forms.ValidationError("Title must be at least 4 characters long.")
        if self.user:
            qs = Listing.objects.filter(owner=self.user, title__iexact=title, status='open')
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("You already have an open listing with this title.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        if len(description) < 10:
            raise forms.ValidationError("Please provide a slightly more detailed description (at least 10 characters).")
        return description