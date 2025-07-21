from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    widget = field.field.widget
    input_type = getattr(widget, 'input_type', None)  # Güvenli şekilde input_type al

    if input_type != 'checkbox':
        existing_classes = widget.attrs.get('class', '')
        widget.attrs['class'] = f'{existing_classes} {css}'.strip()

    return field
