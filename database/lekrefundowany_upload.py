# Zakładam, że bilbioteki pobierzecie z neta.
# Komenda: sudo apt-get install python3-pip
# A potem np. sudo pip3 install -U pandas
# albo sudo pip3 install sqlalchemy. 
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

LekRefundowany = pd.read_csv('leki_z_apteki5.csv').iloc[:, 1:]

# Przed odpaleniem pobierz postgresa na komputer. Musisz utworzyć użytkownika root o haśle root.
# Dla roota musi zostac stworzony database o nazwie lekidb - więcej info w settings.py projektu Django.
engine = create_engine('postgresql://root:root@localhost:5432/lekidb')
LekRefundowany.to_sql('optymalizator_app_lekrefundowany', engine, if_exists='append', index=False)
