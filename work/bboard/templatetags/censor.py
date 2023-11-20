from django import template

register = template.Library()


@register.filter()
def censor(value):
    bad_words = ['пидор', 'пидарасина']
    words = value.split()
    result = []
    for word in words:
        if word in bad_words:
            result.append(word.replace(word[1:], '*' * (len(word) - 1)))
        else:
            result.append(word)
        return ' '.join(result)







