from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import F
from django.core.paginator import Paginator

from .models import LekRefundowany, LicznikWyszukan

from .wyszukiwarka import read
from .substitutes import find_substitutes

def home(request):
    request.session['drugs'] = []
    return render(request, 'home/home.html')

def search(request):
    if request.method != 'GET': return JsonResponse({'success': False, 'error': 'wrong method'})

    q = request.GET.get('q', '')
    print("_______q________")
    print(q)
    print(q == '')
    if q == '': return redirect('home')

    drugs = read(q)

    paginator = Paginator(drugs, 10)
    page_number = min(max(int(request.GET.get('page', 1)), 1), paginator.num_pages)

    context = {
        'query': q if q != None else '',
        'drugs': paginator.get_page(page_number),
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
