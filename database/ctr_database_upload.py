# Zakładam, że bilbioteki pobierzecie z neta.
# Komenda: sudo apt-get install python3-pip
# A potem np. sudo pip3 install -U pandas
# albo sudo pip3 install sqlalchemy. 
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

LicznikLekow = pd.read_csv('ctr_table.csv').iloc[:, 1:]

# Przed odpaleniem pobierz postgresa na komputer. Musisz utworzyć użytkownika root o haśle root.
# Dla roota musi zostac stworzony database o nazwie lekidb - więcej info w settings.py projektu Django.
engine = create_engine('postgresql://root:root@localhost:5432/lekidb')
LicznikLekow.to_sql('optymalizator_app_licznikwyszukan', engine, if_exists='replace', index=False)
