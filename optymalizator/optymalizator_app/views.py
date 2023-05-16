from django.shortcuts import render, redirect
from django.http import JsonResponse
from .wyszukiwarka import read
from django.db.models import F

from .substitutes import find_substitutes
from .models import LekRefundowany, LicznikWyszukan

def home(request):
    request.session['json_list'] = []
    return render(request, 'home/home.html')

def search(request):
    if request.method != 'GET': return JsonResponse({'success': False, 'error': 'wrong method'})

    q = request.GET.get('q', '')
    if q == '': return redirect('home')

    json_list = read(q)

    context = {
        'input_text': q if q != None else '',
        'json_list': json_list if json_list != None else [],
    }
    return render(request, 'search/search.html', context)

def optimize(request):
    if request.method != 'GET': return JsonResponse({'success': False, 'error': 'wrong method'})

    selected = request.GET.get('selected', None)
    if selected == None: redirect('home')

    drug = LekRefundowany.objects.get(id=selected)
    LicznikWyszukan.objects.filter(ean=drug.ean).update(ctr=F('ctr')+1)
    context = { 'drugs': find_substitutes(drug) }
    return render(request, 'optimize/optimize.html', context)
