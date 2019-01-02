from django.db import models

from capybara_forms.models import CapybaraFormsCategory, CapybaraFormsModel


class Category(CapybaraFormsCategory):
    title = models.CharField(
        max_length=100)

    def __str__(self):
        return self.title


class AdvertPublicationPeriod:
    DAYS_10 = 10
    DAYS_20 = 20
    DAYS_30 = 30
    CHOICES = (
        (DAYS_10, '10 days'),
        (DAYS_20, '20 days'),
        (DAYS_30, '30 days')
    )


class Advert(CapybaraFormsModel(Category)):
    title = models.CharField(
        max_length=100)
    price = models.PositiveSmallIntegerField()
    period = models.PositiveIntegerField(choices=AdvertPublicationPeriod.CHOICES)
