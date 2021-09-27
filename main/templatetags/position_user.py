from django import template
from ..models import User
register = template.Library()

@register.simple_tag
def position_user(obj):
  counter = 1
  for category in obj.category.all() :
      if category.position == 0 :
          counter = 0
  if len(obj.category.all()) == 0 :
      counter = 0
  return  counter