import re
import json


def get_data_fields(data):
    result = {}

    for item in data:
        if data[item]:
            key = re.findall(u'^data\[([\w_]+)\]$', item, re.UNICODE)
            if key:
                key = key[0]
                result[key] = data[item]

    return result


def get_filter_conditions(category_data, filter_values):
    result = {}

    for data_item in category_data:
        if 'name' in data_item and 'type' in data_item:
            name = data_item['name']

            if name in filter_values:
                value = filter_values[name]
                modifier = ''

                if name.endswith('_from'):
                    name = name[:-5]
                    modifier = '__gte'

                if name.endswith('_to'):
                    name = name[:-3]
                    modifier = '__lte'

                if data_item['type'] == 'select' and int(value) > 0:
                    result[name + '__value' + modifier] = int(value)
                elif data_item['type'] in ['number', 'number_select'] and float(value) > 0:
                    result[name + '__value' + modifier] = float(value)
                elif data_item['type'] == 'checkbox':
                    result[name + '__value'] = value == 'on'

    return {'data__' + key: result[key] for key in result}


def get_advert_data_for_form_values(category_data, form_data):
    result = {}
    for field in category_data:
        if 'type' in field:
            field_type = field['type']
            if field_type == 'color':
                field_name = 'color'
                display_name = u'Цвет'
            else:
                if 'name' not in field:
                    continue

                field_name = field['name']
                display_name = field['display_name']

            if field_name in form_data:
                row = {
                    'type': field['type'],
                    'display_name': display_name,
                    'value': form_data[field_name]
                }

                if field['type'] == 'select':
                    row['value'], row['display_value'] = json.loads(form_data[field_name])
                    if int(row['value']) == 0:
                        continue

                if field['type'] == 'checkbox':
                    row['value'] = form_data[field_name] == 'on'

                if field['type'] == 'number':
                    row['value'] = float(form_data[field_name].replace(',', '.'))

                result[field_name] = row

    return result


def validate_data(category, data):
    result = []
    # first, check requirement
    for field in category.params:
        if 'required' in field and field['required']:
            valid = field['name'] in data and 'value' in data[field['name']] and data[field['name']]['value']
            if not valid:
                result.append((field['name'], u'Необходимо заполнить поле'))

    return result


def float_to_string(val):
    return str(val).rstrip('0').rstrip('.')
