# Zakładam, że bilbioteki pobierzecie z neta.
# Komenda: sudo apt-get install python3-pip
# A potem np. sudo pip3 install -U pandas
# albo sudo pip3 install sqlalchemy. 
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

DaneLeku = pd.read_csv('dane_o_leku5.csv').iloc[:, 1:]

# Przed odpaleniem pobierz postgresa na komputer. Musisz utworzyć użytkownika root o haśle root.
# Dla roota musi zostac stworzony database o nazwie lekidb - więcej info w settings.py projektu Django.
engine = create_engine('postgresql://root:root@localhost:5432/lekidb')
DaneLeku.to_sql('optymalizator_app_daneleku', engine, if_exists='append', index=False)
