from django.shortcuts import render

from .wyszukiwarka import read

from .substitutes import find_substitutes

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
    if request.method == 'POST':
        selected = request.POST['selected']
        substitutes = find_substitutes(selected)
        context = { "drugs" :  substitutes }
    else:
        context = { "drugs" : [] }
    return render(request, 'optimize/optimize.html', context)
