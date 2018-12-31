from django.contrib import admin

from capybara_forms.forms import CategoryAdminForm

from shop.models import Category, Advert


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm(Category)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Advert)
