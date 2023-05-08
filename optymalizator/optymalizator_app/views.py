from django.shortcuts import render

# TODO: create database model (Kuba)

def home(request):
    return render(request, 'home/home.html')

def search(request):
    if request.method == 'POST':
        input_text = request.POST['input_text']
        print(input_text)
        # TODO: parse input_text into json (Antek)
    return home(request) # TODO: return search results (Mikołaj)

def optimize(request):
    if request.method == 'POST':
        selected = request.POST['selected']
        print(selected)
        # TODO: parse selected into json (Szymon)
    return render(request, 'optimize/optimize.html') # TODO: return optimize results - ui zrobione, ale trzeba jeszcze sparsować kontekst do htmla (Staszek)
