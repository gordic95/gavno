from datetime import datetime
from django import template

register = template.Library()


@register.simple_tag()
def format_date(format_string='%x %d %Y'):
    return datetime.utcnow().strftime(format_string)


@register.simple_tag(takes_context=True)   # takes_context=True - для того, чтобы можно было передавать контекст в тег
def url_replace(context, **kwargs):     # для того, чтобы передать параметры в теги url_replace
    # пример: {% url_replace page=1 %}
    # для того, чтобы передать параметры в теги url_replace
    # пример: {% url_replace page=1 sort=name %}
    # для того, чтобы передать параметры в теги url_replace
    # пример: {% url_replace page=1 sort=name order=desc %}
    # для того, чтобы передать параметры в теги url_replace
    # пример: {% url_replace page=1 sort=name order=desc search=hello %}
    d = context['request'].GET.copy()   # копируем GET
    for k, v in kwargs.items():     # добавляем новые параметры и значения из kwargs в GET и записываем в d
        d[k] = v       # добавляем новые параметры и значения из kwargs в GET и записываем в d
    return d.urlencode()      # возвращаем GET

