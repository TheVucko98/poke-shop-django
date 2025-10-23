from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import *
import re
# Autori: Nikola Milosavljevic 0355/2021
#         Aleksandar Vuckovic  0733/2022


class KartaCreationForm(forms.ModelForm):
    """
        A form for creating a new card.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.add_input(Submit('submit', 'Add Card'))

    class Meta:
        model = Karta
        fields = ['naziv', 'opis', 'cena', 'slika', ]
        labels = {
            'naziv': 'Name',
            'opis': 'Description',
            'cena': 'Price',
            'slika': 'Image',
        }

class KorisnikCreationForm(UserCreationForm):
    """
        A form for creating a new user.
    """
    slika=forms.ImageField(required=False)
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.add_input(Submit('submit', 'Create profile'))
    class Meta:
        model = RegistrovanKorisnik
        fields = ['username','password1', 'password2', 'slika']



class LoginKorisnikForm(AuthenticationForm):
    """
            A form for logging in.
        """
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.add_input(Submit('submit', 'Login'))

    class Meta:
        model = RegistrovanKorisnik
        fields = ['username', 'password']


class ConfirmDeleteForm(forms.Form):
    """
            A form for deletion confirmation.
        """
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.add_input(Submit('submit', 'Delete',css_class='btn btn-danger'))

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

class CheckoutForm(forms.Form):
    """
            A form for filling the customer checkout info.
        """
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email')
    address = forms.CharField(label='Address', max_length=255)
    city = forms.CharField(label='City', max_length=100)
    zip = forms.CharField(label='Postal Code', max_length=10)
    card = forms.CharField(label='Credit Card Number', max_length=19)
    expiry = forms.CharField(label='Expiration Date', max_length=5)
    cvv = forms.CharField(label='CVV', max_length=4)

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Personal Information',
                'name',
                'email'
            ),
            Fieldset(
                'Shipping Address',
                'address',
                'city',
                'zip'
            ),
            Fieldset(
                'Payment Information',
                'card',
                'expiry',
                'cvv'
            ),
            ButtonHolder(
                Submit('submit', 'Order', css_class='btn btn-success')
            )
        )

    def clean_expiry(self):
        """
            This function is used for checking the expiry date of the card.
        """
        expiry = self.cleaned_data['expiry']
        if not re.match(r'^(0[1-9]|1[0-2])\/\d{2}$', expiry):
            raise ValidationError('Expiration date must be in MM/YY format')
        return expiry

    def clean_cvv(self):
        """
            This function is used for checking the CVV of the card.
        """
        cvv = self.cleaned_data['cvv']
        if not re.match(r'^\d{3,4}$', cvv):
            raise ValidationError('CVV must be 3 or 4 digits')
        return cvv

