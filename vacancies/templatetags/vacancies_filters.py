from django import template

register = template.Library()


@register.filter
def vacancy_declension(num):
    unit = int(str(num)[-1])
    tens = int(str(num // 10)[-1])
    if unit == 1 and tens != 1:
        return f'{num} вакансия'
    elif 1 < unit < 5 and tens != 1:
        return f'{num} вакансии'
    else:
        return f'{num} вакансий'


@register.filter
def people_declension(num):
    unit = int(str(num)[-1])
    tens = int(str(num // 10)[-1])
    if 1 < unit < 5 and tens != 1:
        return f'{num} человека'
    else:
        return f'{num} человек'


@register.filter
def convert_to_list(s):
    return s.split(', ')


@register.filter
def response_declension(num):
    unit = int(str(num)[-1])
    tens = int(str(num // 10)[-1])
    if unit == 0:
        return f'Нет откликов'
    elif unit == 1 and tens != 1:
        return f'{num} отклик'
    elif 1 < unit < 5 and tens != 1:
        return f'{num} отклика'
    else:
        return f'{num} откликов'
