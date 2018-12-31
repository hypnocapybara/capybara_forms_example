from capybara_forms.forms import CapybaraFormsModelForm

from shop.models import Advert


class AdvertForm(CapybaraFormsModelForm):
    class Meta:
        model = Advert
        fields = ('title', 'price')
