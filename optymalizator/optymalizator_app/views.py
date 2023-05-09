from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .wyszukiwarka import read

from .substitutes import find_substitutes
from .models import LekRefundowany

def home(request):
    # request.session['input_text'] = ""
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
    selected = request.sesssion["selected"]
    # if request.method == 'POST':
    #     # selected = request.POST['selected']
    #     request.session['selected'] = request.POST['selected']
    #     selected = LekRefundowany.objects.all().get(pk=request.POST['selected'])
    #     context = { "drugs" : find_substitutes(selected) }
    #     print(selected.nazwa)
    #     print("FIND SUBSTITUTES:")
    #     print(find_substitutes(selected))
    #     return render(request, 'optimize/optimize.html', context)
    context = { "drugs" : find_substitutes(selected) }
    return render(request, 'optimize/optimize.html', context)


def get_optimize_results(request):
    if (request.method == 'POST'):
        selected = LekRefundowany.objects.all().get(pk=request.POST['selected'])
        request.session["selected"] = request.POST["selected"]
        return HttpResponse("SUCCESS")
    return HttpResponse("ERROR")