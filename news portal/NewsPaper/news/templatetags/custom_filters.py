from django import template

register = template.Library()

CENSOR_LIST = ['мат', 'сильный мат']


@register.filter(name='censor')
def censor(value):
    text = value.split()
    for word in text:
        if word.lower() in CENSOR_LIST:
            value = value.replace(word, '***')
    return value