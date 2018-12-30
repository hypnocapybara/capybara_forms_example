from capybara_forms.models import SelectData


def render_nested_options(key, is_filter):
    if is_filter:
        result = [u"<option value='0'>Не выбрано</option>"]
    else:
        result = [u"<option value='[0,\"Не выбрано\"]'>Не выбрано</option>"]

    data = SelectData.objects.filter(key=key).order_by('value').values_list('pk', 'value')
    for row in data:
        if is_filter:
            result.append("<option value='%s'>%s</option>" % (
                row[0], row[1]
            ))
        else:
            result.append("<option value='%s'>%s</option>" % (
                '[%s, "%s"]' % row,
                row[1]
            ))

    return '\n'.join(result)
