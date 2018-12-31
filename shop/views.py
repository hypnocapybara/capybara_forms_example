from django.shortcuts import render, get_object_or_404

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
    return render(request, 'list.html', {
        'categories': Category.objects.all(),
        'adverts': Advert.objects.filter(category=category)
    })


def detail(request, item_id):
    pass
