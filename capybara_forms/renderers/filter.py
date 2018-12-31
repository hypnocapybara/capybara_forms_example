import re
from django.template.loader import render_to_string

from capybara_forms.models import SelectData


def _render_filter_string(field, filter_values):
    return render_to_string('capybara_forms/filter/string.html', {'field': field})


def _render_filter_select(field, filter_values):
    if 'nested_on' in field:
        field['nested_prefix'] = field['options']

    if 'nested_on' in field and int(filter_values.get(field['nested_on'], 0)) > 0:
        nested_id = filter_values.get(field['nested_on'])
        field['options'] = SelectData.objects.filter(
            parent_id=nested_id
        ).order_by('value').values_list('pk', 'value')
    elif type(field['options']) is not list:
        field['options'] = SelectData.objects.filter(
            key=field['options']
        ).order_by('value').values_list('pk', 'value')

    if field.get('value') is not None:
        field['value'] = int(field['value'])

    return render_to_string('capybara_forms/filter/select.html', {'field': field})


def _render_filter_number(field, filter_values):
    return render_to_string('capybara_forms/filter/number.html', {'field': field})


def _render_filter_number_select(field, filter_values):
    if 'options' not in field or type(field['options']) is not list:
        field['options'] = []
        if 'start' in field and 'end' in field and 'step' in field:
            start = field['start']
            step = field['step']
            end = field['end']
            current = start
            while current <= end if step > 0 else current >= end:
                field['options'].append(str(current))
                current += step

    field['value'] = field.get('value', '0')
    return render_to_string('capybara_forms/filter/number_select.html',
                            {'field': field})


def _render_filter_checkbox(field, filter_values):
    return render_to_string('capybara_forms/filter/checkbox.html', {'field': field})


FILTER_FIELD_TYPES_TO_FUNCTIONS = {
    'string': _render_filter_string,
    'select': _render_filter_select,
    'number': _render_filter_number,
    'number_select': _render_filter_number_select,
    'checkbox': _render_filter_checkbox,
}


def render_filter_fields(category, filter_values):
    data = category.search_params
    form_groups = {}
    for field in data:
        if 'type' in field and field['type'] in FILTER_FIELD_TYPES_TO_FUNCTIONS:
            if field['name'] in filter_values:
                field['value'] = filter_values[field['name']]

            render_function = FILTER_FIELD_TYPES_TO_FUNCTIONS[field['type']]
            form_groups[field['name']] = render_function(field, filter_values)

    if category.filter_template:
        fields_in_filter = re.findall('{(\w+)}', category.filter_template)
        result = category.filter_template
        for field_name in form_groups:
            if field_name in fields_in_filter:
                result = result.replace('{' + field_name + '}',
                                        '<div class="cpb_form_item">' +
                                        form_groups[field_name] +
                                        '</div>')

        return result
    else:
        form_groups = [
            '<div class="cpb_form_item">' + form_groups[field['name']] + '</div>'
            for field in data if 'type' in field and field['type'] in FILTER_FIELD_TYPES_TO_FUNCTIONS
        ]
        return '\n'.join(form_groups)