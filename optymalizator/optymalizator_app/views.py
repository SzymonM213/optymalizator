from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import F
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import LekRefundowany, LicznikWyszukan, DaneLeku

# from .wyszukiwarka import read
# from .substitutes import find_substitutes

from .search import find_search_results
from .optimize import find_substitutes, find_ref_levels, find_ordinances

def home(request):
    return render(request, 'home/home.html')

def search(request):
    if request.method != 'GET': return JsonResponse({'success': False, 'error': 'wrong method'})

    q = request.GET.get('q', '')
    if q == '': return redirect('home')

    drugs = find_search_results(q)

    paginator = Paginator(drugs, 50)
    page_number = min(max(int(request.GET.get('page', 1)), 1), paginator.num_pages)

    context = {
        'query': q if q != None else '',
        'drugs': paginator.get_page(page_number),
    }
    return render(request, 'search/search.html', context)

def optimize(request):
    if request.method != 'GET': return JsonResponse({'success': False, 'error': 'wrong method'})

    id = request.GET.get('id', None)
    lvl = request.GET.get('lvl', None)

    
    try: drug = LekRefundowany.objects.get(pk=id)
    except: return redirect('home')

    LicznikWyszukan.objects.filter(ean=drug.ean).update(ctr=F('ctr')+1)
    context = {
        'drugs': find_substitutes(drug, lvl),
        'ref_levels': find_ref_levels(drug),
        'ordinances': find_ordinances(drug, lvl),
    }

    return render(request, 'optimize/optimize.html', context)

def get_optimize_results(request):
    if request.method != 'GET': return JsonResponse({'success': False, 'error': 'wrong method'})

    id = request.GET.get('id', None)
    lvl = request.GET.get('lvl', None)
    ord_date = request.GET.get('ord', None)

    try: drug = LekRefundowany.objects.get(pk=id)
    except: return redirect('home')

    return JsonResponse({'drugs': find_substitutes(drug, lvl, ord_date)})

@csrf_exempt
def clear(request):
    if request.method != 'POST': return JsonResponse({'success': False, 'error': 'wrong method'})
    LicznikWyszukan.objects.all().update(ctr=0)
    return redirect('home')

def ref_levels(request):
    if request.method != 'GET': return JsonResponse({'success': False, 'error': 'wrong method'})

    drug_id = request.GET.get('id', None)
    if drug_id == None: return JsonResponse({'success': False, 'error': 'no drug_id'})
    drug = LekRefundowany.objects.get(pk=drug_id)
    if drug == None: return JsonResponse({'success': False, 'error': 'no drug'})

    return JsonResponse({'lvls': find_ref_levels(drug)})
