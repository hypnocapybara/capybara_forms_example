from django import forms

from capybara_forms.renderers.filter import render_filter_fields
from capybara_forms.utils import get_advert_data_for_form_values, \
    validate_data, get_data_fields, get_filter_conditions
from capybara_forms.renderers.form import render_form_fields, \
    render_form_fields_from_model
from capybara_forms.widgets import JSONEditorWidget


class CapybaraFormsModelForm(forms.ModelForm):
    error_css_class = 'error'
    data_errors = {}  # {field_name: error_message}
    category = None
    fields_in_model = []
    fields_in_model_override = {}
    fields_in_filter = []
    fields_in_filter_override = {}

    def __init__(self, category, *args, **kwargs):
        super(CapybaraFormsModelForm, self).__init__(*args, **kwargs)
        self.category = category
        self.data_errors = {}

    def is_valid(self):
        ret = super(CapybaraFormsModelForm, self).is_valid()
        for f in self.errors:
            self.fields[f].widget.attrs.update({
                'class': self.fields[f].widget.attrs.get('class', '') + ' error'
            })

        instance_data = get_data_fields(self.data)
        instance_data = get_advert_data_for_form_values(
            self.category.params, instance_data)
        data_errors = validate_data(self.category, instance_data)
        for error_field, error_message in data_errors:
            self.add_data_error(error_field, error_message)

        if data_errors:
            return False

        return ret

    def add_data_error(self, error_field, error_message):
        if error_field in self.data_errors:
            if error_message not in self.data_errors[error_field]:
                self.data_errors[error_field].append(error_message)
        else:
            self.data_errors[error_field] = [error_message]

    def save(self, commit=True):
        instance = super(CapybaraFormsModelForm, self).save(commit=False)
        instance_data = get_data_fields(self.data)
        instance.data = get_advert_data_for_form_values(self.category.params, instance_data)

        if commit:
            instance.save()

        return instance

    def filter_adverts(self):
        queryset = self._meta.model.objects.filter(category=self.category)
        conditions = get_filter_conditions(
            self.category.search_params, self.fields_in_filter, self.data)
        queryset = queryset.filter(**conditions)
        return queryset

    def render_form(self):
        return render_form_fields_from_model(
            self
        ) + render_form_fields(
            self.category,
            self.instance.data if self.instance.data else {})

    def render_filter(self):
        data_fields = get_data_fields(self.data)
        data_fields.update({
            field: self.data.get(field, '') for field in self.fields_in_filter if field in self.data
        })
        return render_filter_fields(self, data_fields)

    def render_advert_fields(self):
        pass


def CategoryAdminForm(CategoryClass):
    class FormClass(forms.ModelForm):

        class Meta:
            model = CategoryClass
            fields = '__all__'
            widgets = {
                'params': JSONEditorWidget(),
                'search_params': JSONEditorWidget()
            }

        class Media:
            css = { 'all': ('/static/capybara_forms/css/jsoneditor.min.css',)}
            js = ('/static/capybara_forms/js/jsoneditor.min.js', )

    return FormClass
