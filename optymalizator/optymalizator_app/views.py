from django.shortcuts import render
from django.http import JsonResponse
from .wyszukiwarka import read

from .substitutes import find_substitutes
from .models import LekRefundowany, LicznikWyszukan

def home(request):
    request.session['json_list'] = []
    return render(request, 'home/home.html')

def search(request):
    if (request.method == 'POST'):
        request.session['json_list'] = []
        request.session['input_text'] = request.POST['input_text']
        input_text = request.POST['input_text']
        if (input_text == ""):
            return home(request)
        json_list = read(input_text)
        if (json_list == None):
            return home(request)
        context = {
            'json_list': json_list
        }
        request.session['input_text'] = request.POST['input_text']
        request.session['json_list'] = json_list
        return render(request, 'search/search.html', context)

    input_text = request.session.get('input_text')
    json_list = request.session.get('json_list')
    context = {
        'input_text': input_text,
        'json_list': json_list,
    }
    return render(request, 'search/search.html', context)


def get_search_results(request):
    if (request.method == 'POST'):
        request.session['input_text'] = request.POST['input_text']
        request.session['json_list'] = []
        input_text = request.POST['input_text']
        if (input_text == ""):
            JsonResponse({'error': 'empty input'})
        json_list = read(input_text)
        if (json_list == None):
            JsonResponse({'error': 'empty input'})
        request.session['input_text'] = request.POST['input_text']
        request.session['json_list'] = json_list
        res = { 'json_list': json_list }
        return JsonResponse(res, safe=True)
    

def optimize(request):
    selected = request.session["selected"]
    selected = LekRefundowany.objects.all().get(pk=selected)
    context = { "drugs" : find_substitutes(selected) }
    return render(request, 'optimize/optimize.html', context)


def get_optimize_results(request):
    if (request.method == 'POST'):
        request.session["selected"] = request.POST["selected"]
        return JsonResponse({'success': 'true'})
    return JsonResponse({'success': 'false'})
