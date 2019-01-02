from django import forms

from capybara_forms.forms import CapybaraFormsModelForm

from shop.models import Advert


class AdvertForm(CapybaraFormsModelForm):
    fields_in_model = ['title', 'price']
    fields_in_filter = ['price_from', 'price_to']

    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter title'}))

    class Meta:
        model = Advert
        fields = ('title', 'price')
