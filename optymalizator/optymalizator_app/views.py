from django.shortcuts import render

from .wyszukiwarka import read

from .substitutes import find_substitutes
from .models import LekRefundowany

# TODO: poprawić modele (Kuba)

def home(request):
    return render(request, 'home/home.html')

def search(request):
    if (request.method == 'POST'):
        input_text = request.POST['input_text']
        if (input_text == ""):
            return home(request)
        json_list = read(input_text)
        if (json_list == None):
            return home(request)
        context = {
            'json_list': json_list
        }
        return render(request, 'search/search.html', context)  # TODO: ui do wyników wyszukiwania (Mikołaj)
        
    return home(request)

def optimize(request):
    selected = None
    if request.method == 'POST':
        selected = request.POST['selected']
    else: #DEBUG
        selected = LekRefundowany.objects.all().get(pk=420)
    context = { "drugs" : find_substitutes(selected) }
    return render(request, 'optimize/optimize.html', context)
