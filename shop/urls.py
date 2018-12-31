from django.urls import path

from shop.views import *


urlpatterns = [
    path('', index),
    path('add/', add_index),
    path('add/<category_id>/', add),
    path('view/<item_id>/', detail),
    path('<category_id>/', list),
]
