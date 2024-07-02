# custom_filters.py

from django import template

register = template.Library()

@register.filter(name='arabic_numeral')
def arabic_numeral(value):
    """
    Converts Western (Hindu-Arabic) numerals to Arabic-Indic numerals.
    Example:
    Input: 123
    Output: ١٢٣
    """
    arabic_digits = {'0': '٠', '1': '١', '2': '٢', '3': '٣', '4': '٤',
                     '5': '٥', '6': '٦', '7': '٧', '8': '٨', '9': '٩'}
    
    return ''.join(arabic_digits[char] if char in arabic_digits else char for char in str(value))

@register.filter
def get_range(value):
    return range(1, value + 1)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)