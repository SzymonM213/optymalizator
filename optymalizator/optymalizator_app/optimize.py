from .models import LekRefundowany, DaneLeku
from django.db.models import F

def find_substitutes(drug):
    # NOTE:
    # To jest tylko tymczasowe rozwiazanie.
    # Funkcja Szymona obecnie się wykrzacza, bo baza danych była zmieniana

    if drug == None: return None

    active_substance = drug.substancja_czynna
    form = drug.postac
    dose = drug.dawka
    package_content = drug.zawartosc_opakowania

    # the substitutes remain the same regardless of the refundation level and date

    # TODO:

    substitutes = LekRefundowany.objects.filter(substancja_czynna=active_substance)

    return substitutes

def find_ref_levels(drug):
    ean = drug.ean
    lvls_set = DaneLeku.objects.filter(ean=ean)\
                               .values('poziom_odplatnosci')\
                               .order_by('poziom_odplatnosci')
    lvls_list = [d['poziom_odplatnosci'] for d in lvls_set]
    return list(dict.fromkeys(lvls_list))

def find_ordinances(drug, lvl):
    if drug == None or lvl == None: return []
    ean = drug.ean
    ord_set = DaneLeku.objects.filter(ean=ean, poziom_odplatnosci=lvl)\
                              .values('data_rozporzadzenia')\
                              .order_by(F('data_rozporzadzenia').desc())
    ord_list = [d['data_rozporzadzenia'] for d in ord_set]
    return map(lambda x: x.strftime('%Y-%m-%d'), ord_list)
