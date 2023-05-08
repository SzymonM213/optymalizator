from django.shortcuts import render

from .wyszukiwarka import read


# TODO: create database model (Kuba)

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
        return render(request, 'home/search.html', context)
    return home(request) # TODO: return search results (Mikołaj)

def optimize(request):
    if request.method == 'POST':
        selected = request.POST['selected']
        print(selected)
        # TODO: parse selected into json (Szymon)
    return render(request, 'optimize/optimize.html') # TODO: return optimize results - ui zrobione, ale trzeba jeszcze sparsować kontekst do htmla (Staszek)
