from django.shortcuts import render

from .wyszukiwarka import read

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
        return render(request, 'home/search.html', context)  # TODO: ui do wyników wyszukiwania (Mikołaj)
    return home(request)

def optimize(request):
    if request.method == 'POST':
        selected = request.POST['selected']
        print(selected)
        # TODO: zwrócenie w request listy odpowiedników (Szymon)
    return render(request, 'optimize/optimize.html')
