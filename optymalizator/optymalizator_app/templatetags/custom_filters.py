from django import template

register = template.Library()

@register.filter
def elided_page_range(current_page, on_each_side=3, on_ends=1):
    return current_page.paginator.get_elided_page_range(
        number=current_page.number,
        on_each_side=on_each_side,
        on_ends=on_ends,
    )
