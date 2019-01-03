from django.shortcuts import render, get_object_or_404, redirect

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
    if request.method == 'POST':
        form = AdvertForm(category, request.POST.dict())
        if form.is_valid():
            form.save()
            return redirect('/{0}/'.format(category_id))
    else:
        form = AdvertForm(category)

    return render(request, 'add.html', {
        'form': form,
    })


def list(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    form = AdvertForm(category, data=request.GET)

    return render(request, 'list.html', {
        'categories': Category.objects.all(),
        'adverts': form.filter_adverts(),
        'form': form,
    })


def detail(request, item_id):
    item = get_object_or_404(Advert, pk=item_id)
    form = AdvertForm(item.category, instance=item)

    return render(request, 'detail.html', {
        'item': item,
        'form': form
    })
