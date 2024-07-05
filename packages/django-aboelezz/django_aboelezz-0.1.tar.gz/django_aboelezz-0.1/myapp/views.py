from django.shortcuts import render
from .models import MyModel

def my_view(request):
    items = MyModel.objects.all()
    return render(request, 'myapp/my_template.html', {'items': items})
