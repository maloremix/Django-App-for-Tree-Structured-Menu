from django import template
from django.urls import resolve
from menu.models import MenuItem
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    menu = MenuItem.objects.filter(menu__name=menu_name).order_by('id').select_related('parent', 'menu')
    menu_html = ''
    menu_items = {}
    roots = []
    active_item = None

    for item in menu:
        menu_items[item.id] = {
            'name': item.name,
            'url': item.url,
            'parent_id': item.parent_id,
            'children': []
        }

        if item.parent is None:
            roots.append(item.id)

        if item.url + "/" == context['request'].path:
            active_item = item

    for item_id, item in menu_items.items():
        if item['parent_id'] is not None:
            parent = menu_items[item['parent_id']]
            parent['children'].append(item)

    if active_item:
        elements = []
        elements.append(menu_items[active_item.id])
        parent = active_item.parent
        while parent:
            elements.append(menu_items[parent.id])
            parent = parent.parent
        root_active = elements.pop()
        for root in roots:
            if menu_items[root] == root_active:
                menu_html += draw_item(root_active, context, elements)
            else:
                menu_html += f'<li class="nav-item">{draw_link(menu_items[root]["url"], menu_items[root]["name"])}</li>'

    return mark_safe(menu_html)


def draw_item(item, context, elements):
    sub_menu_html = ''
    menu_item_class = 'nav-item'

    if item['children']:
        sub_menu_html += '<ul>'
        for child in item['children']:
            if child in elements:
                sub_menu_html += draw_item(child, context, elements)
            else:
                sub_menu_html += f'<li class="{menu_item_class}">{draw_link(child["url"], child["name"])}</li>'
        sub_menu_html += '</ul>'

    return f'<li class="{menu_item_class}">{draw_link(item["url"], item["name"])}{sub_menu_html}</li>'


def draw_link(url, name):
    return f'<a class="nav-link" href="{url}">{name}</a>'