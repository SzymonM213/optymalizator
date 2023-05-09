import pandas as pd

import os.path

from .models import LekRefundowany

query_set = LekRefundowany.objects.all()
data = list(query_set.values())
df_xlsx = pd.DataFrame(data)

columns = df_xlsx.columns

all_substances = df_xlsx['substancja_czynna'].unique()
all_substances = [subst.lower() for subst in all_substances]

all_names = df_xlsx['nazwa'].unique()
all_names = [name.lower() for name in all_names]
