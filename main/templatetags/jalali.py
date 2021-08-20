from django import template

register = template.Library()
from ..models import jalali_converter


@register.simple_tag
def jalali(date):
    return jalali_converter(date)
