from django.shortcuts import render, get_object_or_404

from capybara_forms.renderers.filter import render_filter_fields
from capybara_forms.utils import get_data_fields
from shop.models import Category, Advert
from shop.forms import AdvertForm


def index(request):
    return render(request, 'index.html', {
        'categories': Category.objects.all()
    })


def add_index(request):
    return render(request, 'add_index.html', {
        'categories': Category.objects.all()
    })


def add(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    form = AdvertForm(category)
    return render(request, 'add.html', {
        'form': form,
    })


def list(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    data_fields = get_data_fields(request.GET)
    filter_html = render_filter_fields(category, data_fields)

    return render(request, 'list.html', {
        'categories': Category.objects.all(),
        'adverts': Advert.objects.filter(category=category),
        'filter_html': filter_html
    })


def detail(request, item_id):
    pass
