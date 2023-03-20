from django.shortcuts import render
from menu.models import Menu

def my_view(request):
    menu_name = 'Main Menu'
    menu = Menu.objects.get(name=menu_name)
    return render(request, 'menu/my_menu.html', {'menu': menu})