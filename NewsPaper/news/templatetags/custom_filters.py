from django import template
import pymorphy3

register = template.Library()
morph = pymorphy3.MorphAnalyzer()


@register.filter()
def censor(value):
    prohibited_words = ('стать', 'озеро', 'прошла', 'факты', 'финал')
    splited_value = value.split()
    for word in splited_value:
        parsed_word = morph.parse(word)[0].normal_form
        if parsed_word in prohibited_words:
            value = value.replace(word, '*' * len(word))
    return value

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()