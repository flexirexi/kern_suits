from django import forms
from .models import UserProfile
from django.core.exceptions import ValidationError
import re


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        user = getattr(self.instance, 'user', None)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

        placeholders = {
            'first_name': "First name",
            "last_name": "Last name",
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
        }

        if 'phone_number' in self.fields:
            self.fields['phone_number'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs.update(
                {'class': 'border-black rounded-0 profile-form-input'}
            )
            self.fields[field].label = False

        if "postcode" in self.fields:
            self.fields["postcode"].widget.attrs.update({
                "inputmode": "numeric",
                "pattern": r"\d{5}",
                "maxlength": "5",
                "title": "5 digits (e.g. 60311)",
            })

        if "phone_number" in self.fields:
            self.fields["phone_number"].widget.attrs.update({
                "inputmode": "tel",
                "pattern": r"[0-9+()\-\s]{7,20}",
                "maxlength": "20",
                "title": "Digits, +, spaces, () and - only",
            })

    def clean_postcode(self):
        val = (self.cleaned_data.get("postcode") or "").strip()
        # DE: 5 digits (anpassen falls EU/International)
        if val and not re.fullmatch(r"\d{5}", val):
            raise ValidationError(
                "Please enter a valid postal code (5 digits)."
            )
        return val

    def clean_phone_number(self):
        val = (self.cleaned_data.get("phone_number") or "").strip()
        # Simple: digits, spaces, +, (), -, 7–20 chars
        if val and not re.fullmatch(r"[+0-9() \-]{7,20}", val):
            raise ValidationError("Please enter a valid phone number.")
        return val

    def save(self, commit=True):
        """Save profile + update linked user's first/last name"""
        profile = super().save(commit=False)
        user = getattr(profile, 'user', None)
        if user:
            user.first_name = self.cleaned_data.get('first_name', '') or ''
            user.last_name = self.cleaned_data.get('last_name', '') or ''
            if commit:
                user.save()
        if commit:
            profile.save()
        return profile
