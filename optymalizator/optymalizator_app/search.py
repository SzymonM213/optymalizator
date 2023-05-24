from .models import LekRefundowany, LicznikWyszukan
from django.db.models import Q, F

import re
from functools import reduce
from operator import and_

def parse_ean(tokens, results):
    rean = r'\d{13}'
    
    ean = set(filter(lambda token: re.fullmatch(rean, token), tokens))

    if len(ean) > 1: return [], []
    if len(ean) == 1: results = results.filter(ean=ean.pop())

    return list(filter(lambda token: not re.fullmatch(rean, token), tokens)), results

def parse_postac(tokens, results):
    rtabl = r'tabl(\.|etk[ai])?'
    rpowl = r'powl(\.|ekan[ae])?'

    tabl = set(filter(lambda token: re.fullmatch(rtabl, token), tokens))
    tokens = list(filter(lambda token: not re.fullmatch(rtabl, token), tokens))

    powl = set(filter(lambda token: re.fullmatch(rpowl, token), tokens))
    tokens = list(filter(lambda token: not re.fullmatch(rpowl, token), tokens))

    rkaps = r'kaps(\.|ułk[ai])?'
    rdoje = r'dojel(\.|itow[ae])?'
    rprze = r'przedł(\.|użonym)?'

    kaps = set(filter(lambda token: re.fullmatch(rkaps, token), tokens))
    tokens = list(filter(lambda token: not re.fullmatch(rkaps, token), tokens))

    doje = set(filter(lambda token: re.fullmatch(rdoje, token), tokens))
    tokens = list(filter(lambda token: not re.fullmatch(rdoje, token), tokens))

    prze = set(filter(lambda token: re.fullmatch(rprze, token), tokens))
    tokens = list(filter(lambda token: not re.fullmatch(rprze, token), tokens))

    rrozt = r'roztw(\.|ór)?'

    rozt = set(filter(lambda token: re.fullmatch(rrozt, token), tokens))
    tokens = list(filter(lambda token: not re.fullmatch(rrozt, token), tokens))

    conditions = []
    if len(tabl) > 0: conditions.append(Q(postac__iregex=rtabl))
    if len(powl) > 0: conditions.append(Q(postac__iregex=rpowl))
    if len(kaps) > 0: conditions.append(Q(postac__iregex=rkaps))
    if len(doje) > 0: conditions.append(Q(postac__iregex=rdoje))
    if len(prze) > 0: conditions.append(Q(postac__iregex=rprze))
    if len(rozt) > 0: conditions.append(Q(postac__iregex=rrozt))
    if (len(conditions) > 0): results = results.filter(reduce(and_, conditions))

    return tokens, results

def parse_dawka(tokens, results):
    rnumb = r'\d+(\.\d+)?'
    runit = r'g|mg|µg|μg|mg\s*/\s*g|mg\s*/\s*ml'

    rdawka = r'({})\s*({})'.format(rnumb, runit)

    dawka = set(filter(lambda token: re.fullmatch(rdawka, token), tokens))
    tokens = list(filter(lambda token: not re.fullmatch(rdawka, token), tokens))

    # NOTE: each dawka in the database contains a space between the number and the unit

    # BUG: Biodroxil (45 g) is not found
    
    i = 0
    while i < len(tokens) - 1:
        tmp = tokens[i] + ' ' + tokens[i + 1]
        if re.fullmatch(rdawka, tmp):
            dawka.add(tmp)
            tokens.pop(i)
            tokens.pop(i)
            continue
        i += 1

    conditions = []
    for token in dawka:
        number = re.search(rnumb, token).group(0)
        unit = re.search(runit, token).group(0)
        conditions.append(Q(dawka__icontains=number + ' ' + unit))

    print(dawka, conditions)

    if len(conditions) > 0: results = results.filter(reduce(and_, conditions))

    return tokens, results

def parse_zawartosc_opakowania(tokens, results):
    rnum = r'\d+'
    rszt = r'szt(\.|uk[ai]?)?'

    rzaw = r'({})\s*({})'.format(rnum, rszt)

    zaw = set(filter(lambda token: re.fullmatch(rzaw, token), tokens))
    tokens = list(filter(lambda token: not re.fullmatch(rzaw, token), tokens))

    i = 0
    while i < len(tokens) - 1:
        tmp = tokens[i] + ' ' + tokens[i + 1]
        if re.fullmatch(rzaw, tmp):
            zaw.add(tmp)
            tokens.pop(i)
            tokens.pop(i)
            continue
        i += 1

    conditions = []
    for token in zaw:
        number = re.search(rnum, token).group(0)
        unit = re.search(rszt, token).group(0)
        conditions.append(Q(zawartosc_opakowania__icontains=number + ' ' + unit))

    if len(conditions) > 0: results = results.filter(reduce(and_, conditions))

    return tokens, results

def find_search_results(query):
    tokens, results = re.split(r'\s+', query.strip()), LekRefundowany.objects.all()

    tokens, results = parse_ean(tokens, results)
    if results.count() == 0: return []

    tokens, results = parse_postac(tokens, results)
    if results.count() == 0: return []

    tokens, results = parse_dawka(tokens, results)
    if results.count() == 0: return []

    tokens, results = parse_zawartosc_opakowania(tokens, results)
    if results.count() == 0: return []

    for token in tokens:
        results = results.filter(
            Q(ean__icontains=token) |
            Q(nazwa__icontains=token) |
            Q(postac__icontains=token) |
            Q(zawartosc_opakowania__icontains=token) |
            Q(substancja_czynna__icontains=token) |
            Q(dawka__icontains=token)
        )

    results = results.order_by(
        F('nazwa').asc(nulls_last=True),
    )

    return [ { 
        'id': result.id,
        'ean': result.ean,
        'nazwa': result.nazwa,
        'postac': result.postac,
        'zawartosc_opakowania': result.zawartosc_opakowania,
        'substancja_czynna': result.substancja_czynna,
        'dawka': result.dawka, } for result in results ]
