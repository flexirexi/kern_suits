from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone',
            'address_line1',
            'address_line2',
            'postal_code',
            'city',
            'country',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'phone': 'Phone',
            'address_line1': 'Street Address 1',
            'address_line2': 'Street Address 2',
            'postal_code': 'Postal Code',
            'city': 'City',
            'country': 'Country',
        }

        self.fields['first_name'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder

            # custom class...
            self.fields[field].widget.attrs['class'] = 'form-control'

            self.fields[field].label = False
