import pandas as pd

df_xlsx = pd.read_excel('leki.xlsx')

columns = df_xlsx.columns

all_substances = df_xlsx['Substancja czynna'].unique()
all_substances = [subst.lower() for subst in all_substances]


all_names = df_xlsx['Nazwa  postać i dawka'].str.split(', ', expand=True)[0].unique()
all_names = [name.lower() for name in all_names]


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