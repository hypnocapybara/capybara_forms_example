import re


def get_data_fields(data):
    result = {}

    for item in data:
        if data[item]:
            key = re.findall(u'^data\[([\w_]+)\]$', item, re.UNICODE)
            if key:
                key = key[0]
                result[key] = data[item]

    # for item in ['price_from', 'price_to', 'search']:
    #     if item in data:
    #         result[item] = data[item]

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


def float_to_string(val):
    return str(val).rstrip('0').rstrip('.')
