from .models import LekRefundowany, LicznikWyszukan
import re

units_pattern = r'µg\)?/dawkę inhalacyjną|µg\)?/dawkę odmierzoną|mg/\d ml|mg/ml|mg|µg|μg|g|ml|j.m.'
unit_scale = { 'g': 1000000, 'mg': 1000, 'µg': 1, 'μg': 1 }

# returns first number included in word or 0, if word doesn't contain any number
def get_number(word):
    match = re.search(r'\d+(\.\d+)?', word)
    if match:
        return match.group()
    else:
        return 0

def get_unit(word):
    match = re.search(units_pattern, word)
    if match:
        return match.group().replace(')', '')
    return None

# returns a dictionary where keys are active ingredients and values are pairs of doses and units
def active_ingr_to_dose(drug):
    if get_unit(drug.dawka) == None:
        return None
    result = {}
    ingredients = drug.substancja_czynna.split(' + ')
    doses = drug.dawka.split('+')
    if len(doses) == 1:
        result[drug.substancja_czynna] = (get_number(drug.dawka), get_unit(drug.dawka))
        return result
    for i in range(len(ingredients)):
        if get_unit(doses[i]) == None:
            result[ingredients[i]] = (get_number(doses[i]), get_unit(doses[-1]))
        else:
            result[ingredients[i]] = (get_number(doses[i]), get_unit(doses[i]))

def in_range(drug_amount, sub_amount):
    return drug_amount <= sub_amount and drug_amount * 1.1 >= sub_amount

def compare_active_ingr_amount(drug, sub):
    if drug[1] == sub[1]:
        return float(drug[0]) == float(sub[0])
    else:
        if drug[1][-1] == 'g' and sub[1][-1] == 'g':
            (float(drug[0]) * unit_scale[drug[1]]) == (float(sub[0]) * unit_scale[sub[1]])
    return False

def get_amount(amount):
    return int(amount.split(' ')[0])

def find_substitutes(drug):
    if drug == None:
        return []
    units = int(drug.zawartosc_opakowania.split(' ')[0])
    drug_ingrs = active_ingr_to_dose(drug)
    drug_amount = get_amount(drug.zawartosc_opakowania)

    substitutes = []
    for substitute in LekRefundowany.objects.all().filter(postac=drug.postac).exclude(pk=drug.pk):
        sub_ingrs = active_ingr_to_dose(substitute)
        if sub_ingrs == None:
            continue
        for ingr in drug_ingrs.keys():
            if ingr not in sub_ingrs.keys():
                break
            elif not compare_active_ingr_amount(drug_ingrs[ingr], sub_ingrs[ingr]):
                break
            elif not in_range(drug_amount, get_amount(substitute.zawartosc_opakowania)):
                break
            else:
                substitutes.append(substitute)
            
    return sorted(substitutes, key=lambda x: (x.wysokosc_doplaty, x.nazwa))