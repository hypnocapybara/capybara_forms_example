from django.db import models
from django.contrib.postgres.fields import JSONField


class CapybaraFormsCategory(models.Model):
    params = JSONField(verbose_name='Category fields', default=dict, null=True)
    search_params = JSONField(verbose_name='Filter fields', default=dict, null=True)
    form_template = models.TextField(
        blank=True, null=True)
    filter_template = models.TextField(
        blank=True, null=True)

    class Meta:
        abstract = True


def CapybaraFormsModel(CategoryModel):
    class CapybaraFormsAdvertClass(models.Model):
        category = models.ForeignKey(
            CategoryModel,
            on_delete=models.CASCADE)
        data = JSONField(
            blank=True, null=True,
            verbose_name='Category fields data')

        fields_in_model = []  # Fields from model, that needs to be rendered with form.render_fields
        fields_in_filter = []  # Filter fields from model, that needs to be rendered in filter

        class Meta:
            abstract = True

    return CapybaraFormsAdvertClass


class SelectData(models.Model):
    key = models.CharField(
        max_length=80)
    value = models.CharField(
        max_length=255)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True, null=True)

    def __unicode__(self):
        return u"%s : %s" % (self.key, self.value)
