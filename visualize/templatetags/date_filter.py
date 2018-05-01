from django import template

register = template.Library()

@register.filter
def date_parse(value):
	return " ".join(value.split("T")).rstrip("Z")
