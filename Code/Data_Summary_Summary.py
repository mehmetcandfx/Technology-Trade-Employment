import pandas as pd
import os
import utilities as u
import eurostat

db=["EARN_SES06_14","EARN_SES10_14","EARN_SES14_14","EARN_SES18_14"]



df=pd.DataFrame()
for ds in db:
    dftemp = pd.DataFrame({
        'Dataset': [ds for i in eurostat.get_pars(ds)],
        'Year': [ 2000+int(ds[-5:-3]) for i in eurostat.get_pars(ds)], 
        'Category' : eurostat.get_pars(ds),
        '#ofUniques': [len(eurostat.get_par_values(ds, i)) for i in  eurostat.get_pars(ds)],
        'Uniques': [eurostat.get_par_values(ds, i) for i in  eurostat.get_pars(ds)]
        })
    df = pd.concat([df, dftemp], ignore_index=True)
print(df)

