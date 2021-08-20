from django import template
from ..models import User
register = template.Library()

@register.simple_tag
def define(*args):
  valueresult = False
  for result in args[0].followers.all():
    if result == args[1]:
      valueresult=True
  return valueresult