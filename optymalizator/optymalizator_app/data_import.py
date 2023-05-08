import pandas as pd

import os.path

from .models import LekRefundowany

query_set = LekRefundowany.objects.all()
data = list(query_set.values())
df_xlsx = pd.DataFrame(data)

# full_path = os.path.abspath('optymalizator_app/leki.xlsx')
# df_xlsx = pd.read_excel(full_path)

columns = df_xlsx.columns

all_substances = df_xlsx['substancja_czynna'].unique()
all_substances = [subst.lower() for subst in all_substances]


all_names = df_xlsx['nazwa'].unique()
all_names = [name.lower() for name in all_names]

# values_to_corresponding_columns = {
#     'ean': 'Numer GTIN lub inny kod jednoznacznie identyfikujący produkt',
#     'name': 'Nazwa  postać i dawka',
#     'form': 'Nazwa  postać i dawka',
#     'dose': 'Nazwa  postać i dawka',
#     'substance': 'Substancja czynna',
#     'content': 'Zawartość opakowania',
# }

# http_and_columns = {
#     'Substancja czynna': 'substancja_czynna',
#     'Nazwa  postać i dawka': 'nazwa_postac_dawka',
#     'Zawartość opakowania': 'zawartosc',
#     'Numer GTIN lub inny kod jednoznacznie identyfikujący produkt': 'ean',
# }


# Returned columns: +"ean": "String",
#                   +"nazwa": "String",
#                   -"dawka": "String"
#                   +"postac": "String"
#                   +"substancja_czynna": "String"
#                   +"zawartosc": "String"


# Columns in df:
# 'LP' 
# 'Substancja czynna',                                                          SUBSTANCJA_CZYNNA
# 'Nazwa  postać i dawka',                                                      NAZWA, POSTAC (oddzielone przecinkami)
# 'Zawartość opakowania',                                                       ZAWARTOSC
# 'Numer GTIN lub inny kod jednoznacznie identyfikujący produkt',               EAN
# 'Termin wejścia w życie decyzji', 
# 'Okres obowiązywania decyzji',
# 'Grupa limitowa', 
# 'Urzędowa cena zbytu', 
# 'Cena hurtowa brutto',
# 'Cena detaliczna', 
# 'Wysokość limitu finansowania',
# 'Zakres wskazań objętych refundacją',
# 'Zakres wskazań pozarejestracyjnych objętych refundacją',
# 'Poziom odpłatności', 
# 'Wysokość dopłaty świadczeniobiorcy'],
